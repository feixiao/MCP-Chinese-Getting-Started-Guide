"""MCP 客户端最小示例（通过 STDIO 调用本地工具服务）

本文件演示如何：
1. 使用 `stdio_client` 启动并连接一个本地的 MCP 服务（由 `web_search.py` 提供工具）。
2. 初始化会话，列出工具，然后调用其中的一个工具。

目录结构假定同级存在 `web_search.py`，其中定义了经 FastMCP 暴露的 `web_search` 工具。

运行步骤：
    uv sync                  # 安装依赖（或使用你已有的虚拟环境）
    python mcp_getting_started/main.py

关键概念说明：
- StdioServerParameters: 指定如何启动服务器端进程（命令 + 参数 + 可选环境变量）。
- stdio_client: 建立与服务器的双工 STDIO 通道，获得 (stdio, write)。
- ClientSession: 基于协议封装的高层对象，提供 initialize / list_tools / call_tool 等方法。

扩展思路：
- 可以在 `web_search.py` 中继续添加多个 `@app.tool()` 工具，再次运行本客户端即可自动列出。
- 若需要改为 HTTP/SSE 形式，可替换为对应的传输层客户端实现。

注意：
- 本示例聚焦客户端调用，不包含服务端实现；服务端示例应在 `web_search.py`。
- 生产环境中请补充异常处理（连接失败、工具不存在、超时等）。
"""

import logging
import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters



# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 为 stdio 连接创建服务器参数：启动一个提供工具的 MCP 服务器进程
server_params = StdioServerParameters(
    # 服务器执行的命令，这里我们使用 uv 来运行 web_search.py
    command='uv',
    # 运行的参数
    args=['run', 'web_search.py'],
    # 环境变量，默认为 None，表示使用当前环境变量
    # env=None
)


async def main():
    # 创建 stdio 客户端
    # 建立与服务器的 stdio 连接
    async with stdio_client(server_params) as (stdio, write):
        # 创建 ClientSession 对象
        async with ClientSession(stdio, write) as session:
            # 初始化 ClientSession
            await session.initialize()

            # 列出可用的工具
            response = await session.list_tools()
            print(response)

            # 调用工具
            response = await session.call_tool('web_search', {'query': '今天杭州天气'})
            print(response)


if __name__ == '__main__':
    asyncio.run(main())