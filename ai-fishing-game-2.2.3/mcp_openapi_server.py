import httpx
from fastmcp import FastMCP

# 加载 OpenAPI 规格（假设放在同目录下）
with open("openapi.json", "r") as f:
    import json
    spec = json.load(f)

# 创建 HTTP 客户端，指向你正在运行的 HTTP API 服务
client = httpx.Client(base_url="http://127.0.0.1:8001")

# 一键生成 MCP 服务器
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    name="AI钓鱼游戏 MCP"
)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8002)