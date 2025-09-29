"""开发时一键启动 Django 后端与 Vite 前端的辅助脚本。"""
from __future__ import annotations

import argparse
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"


class ProcessHandle:
    """对子进程进行封装，便于统一终止。"""

    def __init__(self, name: str, popen: subprocess.Popen):
        self.name = name
        self.popen = popen

    def terminate(self) -> None:
        if self.popen.poll() is not None:
            return

        try:
            if os.name != "nt":
                os.killpg(self.popen.pid, signal.SIGTERM)
            else:
                self.popen.send_signal(signal.CTRL_BREAK_EVENT)
        except Exception:
            self.popen.terminate()

        try:
            self.popen.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.popen.kill()


def ensure_directory(path: Path, description: str) -> None:
    if not path.exists():
        raise SystemExit(f"未找到 {description} 目录：{path}")


def ensure_command_available(command: str) -> str:
    resolved = shutil.which(command)
    if resolved is None:
        raise SystemExit(f"未找到命令：{command}，请确认已安装并加入 PATH")
    return resolved


def ensure_frontend_dependencies(npm_executable: str) -> None:
    node_modules = FRONTEND_DIR / "node_modules"
    plugin_path = node_modules / "@vitejs" / "plugin-react"

    if node_modules.exists() and plugin_path.exists():
        return

    print("[frontend] 检测到依赖缺失，正在安装...", flush=True)
    subprocess.check_call([npm_executable, "install"], cwd=str(FRONTEND_DIR))
    print("[frontend] 依赖安装完成。", flush=True)


def ensure_port_available(
    host: str,
    port_value: str,
    *,
    description: str,
    user_specified: bool,
) -> int:
    try:
        start_port = int(port_value)
    except ValueError:
        raise SystemExit(f"{description} 端口参数无效：{port_value}")

    max_attempts = 20
    for offset in range(max_attempts):
        candidate = start_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, candidate))
            except OSError:
                if user_specified:
                    raise SystemExit(
                        f"{description} 端口 {candidate} 已被占用，请释放该端口或修改参数。"
                    )
                continue
        if offset != 0:
            print(
                f"[{description}] 端口 {start_port} 已被占用，自动切换到 {candidate}。",
                flush=True,
            )
        return candidate

    raise SystemExit(
        f"未能在 {start_port}-{start_port + max_attempts - 1} 范围内找到可用的 {description} 端口，请手动指定空闲端口。"
    )


def popen_command(
    command: Iterable[str],
    cwd: Path,
    env: Optional[Dict[str, str]] = None,
) -> subprocess.Popen:
    kwargs = {
        "cwd": str(cwd),
        "env": env,
        "stdout": None,
        "stderr": None,
        "stdin": None,
    }
    if os.name != "nt":
        kwargs["start_new_session"] = True
    else:
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    return subprocess.Popen(list(command), **kwargs)


def run_migrate(python_executable: str, extra_args: List[str]) -> None:
    command = [python_executable, "manage.py", "migrate", *extra_args]
    print("[backend] 执行 migrate...", flush=True)
    subprocess.check_call(command, cwd=str(BACKEND_DIR))
    print("[backend] migrate 完成。", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="同时启动 Django + Vite 开发服务器")
    parser.add_argument("--backend-host", default="127.0.0.1", help="Django 开发服务器绑定地址")
    parser.add_argument("--backend-port", default="8000", help="Django 开发服务器端口")
    parser.add_argument("--frontend-host", default="127.0.0.1", help="Vite 开发服务器绑定地址")
    parser.add_argument("--frontend-port", default="5173", help="Vite 开发服务器端口")
    parser.add_argument("--npm-command", default="npm", help="用于启动前端的 npm/yarn/pnpm 命令")
    parser.add_argument("--backend-only", action="store_true", help="仅启动 Django 开发服务器")
    parser.add_argument("--frontend-only", action="store_true", help="仅启动 Vite 开发服务器")
    parser.add_argument("--no-migrate", action="store_true", help="启动 Django 前跳过 migrate")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="启用 Django 自动重载（默认关闭以避免父进程提前退出）",
    )
    parser.add_argument(
        "--backend-args",
        nargs=argparse.REMAINDER,
        default=[],
        help="附加到 manage.py runserver 的参数，使用 --backend-args 后的内容将原样透传",
    )
    args = parser.parse_args()

    if args.backend_only and args.frontend_only:
        raise SystemExit("--backend-only 与 --frontend-only 不能同时使用")

    ensure_directory(BACKEND_DIR, "backend")
    if not args.backend_only:
        ensure_directory(FRONTEND_DIR, "frontend")

    processes: List[ProcessHandle] = []
    exit_code = 0
    stop_event = threading.Event()
    try:
        backend_port: Optional[int] = None
        if not args.frontend_only:
            backend_port = ensure_port_available(
                args.backend_host,
                args.backend_port,
                description="backend",
                user_specified="--backend-port" in sys.argv,
            )

        frontend_port: Optional[int] = None
        if not args.backend_only:
            frontend_port = ensure_port_available(
                args.frontend_host,
                args.frontend_port,
                description="frontend",
                user_specified="--frontend-port" in sys.argv,
            )

        if not args.frontend_only:
            python_exec = sys.executable or "python"
            if not args.no_migrate:
                run_migrate(python_exec, [])

            if backend_port is None:
                raise RuntimeError("backend_port 未正确初始化")

            backend_command = [
                python_exec,
                "manage.py",
                "runserver",
                f"{args.backend_host}:{backend_port}",
            ]
            if not args.reload and "--noreload" not in args.backend_args:
                backend_command.append("--noreload")
            backend_command.extend(args.backend_args)
            print(f"[backend] 启动命令：{' '.join(backend_command)}", flush=True)
            backend_proc = popen_command(backend_command, BACKEND_DIR)
            processes.append(ProcessHandle("backend", backend_proc))

        if not args.backend_only:
            npm_executable = ensure_command_available(args.npm_command)
            ensure_frontend_dependencies(npm_executable)

            if frontend_port is None:
                raise RuntimeError("frontend_port 未正确初始化")

            backend_port_for_frontend = backend_port if backend_port is not None else int(args.backend_port)
            frontend_env = os.environ.copy()
            frontend_env.update(
                {
                    "BACKEND_HOST": args.backend_host,
                    "BACKEND_PORT": str(backend_port_for_frontend),
                    "BACKEND_ORIGIN": f"http://{args.backend_host}:{backend_port_for_frontend}",
                    "FRONTEND_HOST": args.frontend_host,
                    "FRONTEND_PORT": str(frontend_port),
                }
            )

            frontend_command = [
                npm_executable,
                "run",
                "dev",
                "--",
                "--host",
                args.frontend_host,
                "--port",
                str(frontend_port),
            ]
            print(f"[frontend] 启动命令：{' '.join(frontend_command)}", flush=True)
            frontend_proc = popen_command(frontend_command, FRONTEND_DIR, frontend_env)
            processes.append(ProcessHandle("frontend", frontend_proc))

        if not processes:
            print("未选择任何进程启动。使用 --help 查看可选项。", flush=True)
            return

        def wait_for_quit() -> None:
            try:
                prompt = "\n输入 q 后回车可同时停止前后端服务。\n"
                if sys.stdin and sys.stdin.isatty():
                    print(prompt, end="", flush=True)
                for line in sys.stdin:
                    if line.strip().lower() == "q":
                        print("收到 q 指令，准备退出...", flush=True)
                        stop_event.set()
                        break
            except Exception:
                pass

        input_thread = threading.Thread(target=wait_for_quit, daemon=True)
        input_thread.start()

        while processes and not stop_event.is_set():
            for proc in processes[:]:
                ret = proc.popen.poll()
                if ret is None:
                    continue

                if ret != 0:
                    print(f"[{proc.name}] 以非零状态码 {ret} 退出", flush=True)
                    exit_code = exit_code or ret
                else:
                    print(f"[{proc.name}] 已退出", flush=True)

                processes.remove(proc)

            if exit_code or not processes:
                break

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n收到中断信号，正在优雅退出...", flush=True)
        stop_event.set()
    finally:
        stop_event.set()
        for proc in processes:
            proc.terminate()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
