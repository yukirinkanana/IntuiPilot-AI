# Django + DRF + Vite(React/TS) 分离式脚手架

## 目录
```
django-react-starter/
├─ backend/              # Django + DRF 后端 (SQLite, JWT, CORS)
│  ├─ backend/           # Django 项目设置
│  ├─ apps/core/         # 示例应用：/api/health
│  ├─ manage.py
│  ├─ requirements.txt
│  └─ .env.example
└─ frontend/             # Vite + React + TypeScript 前端
   ├─ index.html
   ├─ vite.config.ts     # 代理 /api -> http://127.0.0.1:8000
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
```

### 1) 后端
```bash
cd backend
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt

# 初始化环境变量
cp .env.example .env  # Windows 可用：copy .env.example .env

# 数据库迁移 & 启动
python manage.py migrate
python manage.py runserver 8000
```

后端健康检查：浏览器打开 http://127.0.0.1:8000/api/health/ 应返回：`{"status":"ok"}`

### 2) 前端（新开一个终端窗口）
```bash
cd frontend
npm install
npm run dev
```
前端地址： http://127.0.0.1:5173/  
该开发服务器通过代理把 `/api/*` 请求转发到 `http://127.0.0.1:8000`，无需额外配置 CORS。

## 自检清单
- ✅ `http://127.0.0.1:8000/api/health/` 返回 `{"status":"ok"}`
- ✅ `http://127.0.0.1:5173/` 能看到前端页面，点击按钮可获取健康状态
- ✅ 控制台无 404/500/跨域错误

## 常见问题
- **Node 未安装/未入 PATH**：安装 Node.js LTS，重开终端，确保 `node -v` 正常。
- **端口占用**：修改 `backend/backend/settings.py` 中 `ALLOWED_HOSTS` 或换端口；前端端口可在 `vite.config.ts` 设置。
- **CORS**：本模板已启用 `django-cors-headers`，默认允许所有源；生产环境请改为白名单。
