import React, { useState } from "react";
import api from "../lib/api";

export default function Home() {
  const [status, setStatus] = useState<string>("(未检查)");

  async function checkHealth() {
    try {
      const res = await api.get("/health/");
      setStatus(JSON.stringify(res.data));
    } catch (e: any) {
      setStatus("请求失败：" + (e?.message || "未知错误"));
      console.error(e);
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: "40px auto", padding: 24 }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>Django + React 分离式模板</h1>
      <p style={{ opacity: 0.9, lineHeight: 1.6 }}>前端通过 Vite 代理访问后端 /api。点击下方按钮测试后端健康检查。</p>
      <button onClick={checkHealth} style={{ padding: "8px 16px", borderRadius: 8, border: "1px solid #ddd" }}>
        检查 /api/health
      </button>
      <pre style={{ background: "#111", color: "#eee", padding: 12, borderRadius: 8, marginTop: 16 }}>
{status}
      </pre>
    </div>
  );
}
