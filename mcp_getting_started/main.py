import httpx
from mcp.server import FastMCP

# 先创建 FastMCP 实例，供装饰器使用
app = FastMCP('web-search')


@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """

    async with httpx.AsyncClient() as client:
        # response = await client.post(
        #     'https://open.bigmodel.cn/api/paas/v4/tools',
        #     headers={'Authorization': '换成你自己的API KEY'},
        #     json={
        #         'tool': 'web-search-pro',
        #         'messages': [
        #             {'role': 'user', 'content': query}
        #         ],
        #         'stream': False
        #     }
        # )

        # res_data = []
        # for choice in response.json()['choices']:
        #     for message in choice['message']['tool_calls']:
        #         search_results = message.get('search_result')
        #         if not search_results:
        #             continue
        #         for result in search_results:
        #             res_data.append(result['content'])

        # return '\n\n\n'.join(res_data)
        return "这是模拟的搜索结果内容。"

def main():
    # 运行 FastMCP 服务器
    app.run(transport='stdio')


if __name__ == "__main__":
    main()
