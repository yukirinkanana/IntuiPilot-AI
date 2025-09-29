# Django + DRF + Vite(React/TS) 分离式脚手架

## 目录
```text
django-react-starter/
├─ backend/ # Django + DRF 后端 (SQLite, JWT, CORS)
│  ├─ backend/            # Django 项目设置
│  ├─ apps/core/          # 示例应用：/api/health
│  ├─ manage.py
│  ├─ requirements.txt
│  └─ .env.example
└─ frontend/ # Vite + React + TypeScript 前端
   ├─ index.html
   ├─ vite.config.ts      # 代理 /api -> http://127.0.0.1:8000
   └─ src/
      ├─ main.tsx
      ├─ App.tsx
      ├─ pages/Home.tsx
      └─ lib/api.ts
```



## 一键启动（开发）
### 0) 安装前置
- Python 3.10+（建议 3.11/3.12）
- Node.js LTS（含 npm）
- Windows 建议使用 PowerShell；macOS/Linux 使用 bash/zsh。

验证：
```bash
python --version
node -v
npm -v
# 后端虚拟环境
cd backend
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt

# 初始化环境变量
cp .env.example .env  # Windows 可用：copy .env.example .env

# 返回仓库根目录
cd ..

# 前端依赖
cd frontend
npm install
cd ..

python runserver.py
首次执行会自动运行 python manage.py migrate，并在缺少 node_modules 时自动执行前端依赖安装。

可通过 --backend-only 或 --frontend-only 仅启动单侧服务。

默认前端监听 127.0.0.1:5173，后端监听 127.0.0.1:8000，可用 --frontend-port、--backend-port 修改。

Django 服务默认以 --noreload 启动，避免父进程过早退出；若需启用自动重载，请追加 --reload。

后端健康检查：浏览器打开 http://127.0.0.1:8000/api/health/ 应返回：{"status":"ok"}

前端地址： http://127.0.0.1:5173/
开发服务器通过代理把 /api/* 请求转发到 http://127.0.0.1:8000，无需额外配置 CORS。