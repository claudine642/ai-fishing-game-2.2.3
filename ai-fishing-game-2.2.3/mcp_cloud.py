import os
from fastmcp import FastMCP

from fishing import cmd as fishing_cmd
from detective import cmd as detective_cmd

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
    return detective_cmd(action)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
