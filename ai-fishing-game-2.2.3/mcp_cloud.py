import os
from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

from fishing import cmd as fishing_cmd
from detective import cmd as detective_cmd
from detective import new_game as detective_new_game

# 创建独立的 FastAPI 应用
app = FastAPI(title="AI游戏集合")

# 创建 MCP 服务器并挂载到 /sse 路径
mcp = FastMCP("AI游戏集合")

@mcp.tool
def play_fishing(action: str, times: int = 1) -> str:
    """在文字钓鱼游戏中执行动作。可用：help, status, cast, buy, sell..."""
    results = []
    for _ in range(times):
        results.append(fishing_cmd(action))
    return "\n".join(results)

@mcp.tool
def play_detective(action: str) -> str:
    """在蓝玫瑰庄园推理游戏中执行动作。可用：help, status, look, talk, ask..."""
    if action.strip().lower() == "new_game":
        return detective_new_game()
    return detective_cmd(action)

@mcp.tool
def ping() -> str:
    """MCP 层面测试连接"""
    return "pong"

# 将 MCP 的 SSE 端点挂载到 /sse
app.mount("/sse", mcp.sse_app())

# 健康检查端点 —— cron-job 访问这个
@app.get("/ping")
async def health_ping():
    return {"status": "ok", "service": "ai-games"}

# 根路径
@app.get("/")
async def root():
    return {"message": "AI游戏集合运行中，MCP端点在 /sse，健康检查在 /ping"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)