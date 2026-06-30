import os
from fastmcp import FastMCP

from fishing import cmd as fishing_cmd
from detective import cmd as detective_cmd
from detective import new_game as detective_new_game

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)