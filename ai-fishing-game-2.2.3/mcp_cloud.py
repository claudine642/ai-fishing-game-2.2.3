import os
from fastmcp import FastMCP
from fishing import cmd as fishing_cmd
from detective import cmd as detective_cmd
from detective import new_game as detective_new_game
from mystery import cmd as mystery_cmd

mcp = FastMCP("AI游戏集合")

@mcp.tool
def play_fishing(action: str, times: int = 1) -> str:
    """钓鱼游戏"""
    results = []
    for _ in range(times):
        results.append(fishing_cmd(action))
    return "\n".join(results)

@mcp.tool
def play_detective(action: str) -> str:
    """侦探游戏"""
    if action.strip().lower() == "new_game":
        return detective_new_game()
    return detective_cmd(action)

@mcp.tool
def play_mystery(action: str) -> str:
    """密室逃脱"""
    return mystery_cmd(action)

@mcp.tool
def ping() -> str:
    """MCP 层面测试连接"""
    return "pong"

# 添加普通 HTTP 健康检查端点
app = mcp.app
@app.get("/ping")
async def health_ping():
    return {"status": "ok", "service": "ai-games"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)