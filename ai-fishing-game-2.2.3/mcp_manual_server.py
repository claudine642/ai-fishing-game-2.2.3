from fastmcp import FastMCP
import httpx

mcp = FastMCP("AI钓鱼游戏 MCP")

@mcp.tool
def play_fishing(action: str, times: int = 1) -> str:
    """
    在文字钓鱼游戏中执行动作。
    可用动作：help, status, cast, buy, sell, inventory 等。
    """
    client = httpx.Client(base_url="http://127.0.0.1:8001", timeout=10.0)
    resp = client.post("/fish", json={"action": action, "times": times})
    data = resp.json()
    return data.get("output", "无返回结果")

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8002)