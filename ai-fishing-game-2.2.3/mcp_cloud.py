import os
from fastmcp import FastMCP
from fishing import cmd

mcp = FastMCP("AI钓鱼游戏")

@mcp.tool
def play_fishing(action: str, times: int = 1) -> str:
    """
    在文字钓鱼游戏中执行动作。
    可用动作：help, status, cast, buy, sell, inventory 等。
    """
    results = []
    for _ in range(times):
        results.append(cmd(action))
    return "\n".join(results)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
