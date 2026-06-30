import os
from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

from fishing import cmd as fishing_cmd
from detective import cmd as detective_cmd
from detective import new_game as detective_new_game

app = FastAPI(title="AI游戏集合")
mcp = FastMCP("AI游戏集合")

@mcp.tool
def play_fishing(action: str, times: int = 1) -> str:
    results = []
    for _ in range(times):
        results.append(fishing_cmd(action))
    return "\n".join(results)

@mcp.tool
def play_detective(action: str) -> str:
    if action.strip().lower() == "new_game":
        return detective_new_game()
    return detective_cmd(action)

@mcp.tool
def ping() -> str:
    return "pong"

# 挂载 MCP 的 SSE 端点
app.mount("/sse", mcp.sse_app())

@app.get("/ping")
async def health_ping():
    return {"status": "ok", "service": "ai-games"}

@app.get("/")
async def root():
    return {"message": "AI游戏集合运行中，MCP端点在 /sse，健康检查在 /ping"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)