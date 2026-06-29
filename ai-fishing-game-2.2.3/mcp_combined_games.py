#!/usr/bin/env python3
"""
蓝玫瑰庄园 + 钓鱼游戏 · 合并 MCP 服务器
支持 stdio 和 SSE (HTTP) 两种启动模式。
"""

import asyncio
import sys
import os

# 确保当前目录可导入
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import detective
import fishing

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 创建 MCP 服务器实例
server = Server("combined-games")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """向 AI 客户端注册所有游戏工具"""
    return [
        # 侦探游戏
        types.Tool(
            name="play_detective",
            description=(
                "执行蓝玫瑰庄园侦探游戏的一条指令。"
                "可用指令：help, status, look, look <物品>, go <场景>, "
                "talk <NPC>, ask <NPC> <话题>, clues, timeline, "
                "arrange <卡1> <卡2>..., accuse <嫌疑人> <手法>。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "侦探游戏指令"}
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="reset_detective",
            description="重置蓝玫瑰庄园侦探游戏，开启全新一局（清除存档）。",
            inputSchema={"type": "object", "properties": {}},
        ),
        # 钓鱼游戏
        types.Tool(
            name="play_fishing",
            description=(
                "执行钓鱼游戏的一条指令。"
                "具体指令请参考该游戏的 help 输出。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "钓鱼游戏指令"}
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="reset_fishing",
            description="重置钓鱼游戏，开启新的一局（清除钓鱼存档）。",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """处理工具调用分发"""
    
    if name == "play_detective":
        command = arguments.get("command")
        if not command:
            return [types.TextContent(type="text", text="错误：请提供侦探游戏指令。")]
        result = detective.cmd(command)
        return [types.TextContent(type="text", text=result)]
    
    if name == "reset_detective":
        result = detective.new_game()
        return [types.TextContent(type="text", text=result)]
    
    if name == "play_fishing":
        command = arguments.get("command")
        if not command:
            return [types.TextContent(type="text", text="错误：请提供钓鱼游戏指令。")]
        # 如果 fishing 模块的函数名不是 cmd，请修改下面这行
        result = fishing.cmd(command)
        return [types.TextContent(type="text", text=result)]
    
    if name == "reset_fishing":
        # 如果 fishing 模块的重置函数名不是 new_game，请修改下面这行
        result = fishing.new_game()
        return [types.TextContent(type="text", text=result)]
    
    raise ValueError(f"未知工具: {name}")

# ========== 启动入口 ==========
# 支持两种模式：
# 1. 直接运行（默认）-> stdio 模式（用于本地 Claude Desktop 等）
# 2. 带参数 --sse      -> SSE 模式（用于云端部署）

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式（HTTP 服务）
        import uvicorn
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
        from starlette.middleware.cors import CORSMiddleware

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request.send) as streams:
                await server.run(streams[0], streams[1], server.create_initialization_options())

        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request.send)
            return JSONResponse({"status": "ok"})

        app = Starlette(routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages/", endpoint=handle_messages, methods=["POST"]),
        ])
        # 允许跨域（方便浏览器或其他客户端访问）
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

        print("🚀 启动 SSE 服务器，监听 0.0.0.0:8000")
        print("   SSE 端点: http://<你的IP>:8000/sse")
        print("   消息端点: http://<你的IP>:8000/messages/")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # 默认 stdio 模式（本地客户端）
        asyncio.run(mcp.server.stdio.stdio_server().run(server))