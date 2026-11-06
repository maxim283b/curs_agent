"""Проверить запуск MCP по stdio без LLM и промышленного симулятора."""
import asyncio
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main() -> None:
    transport = StdioTransport(
        command=sys.executable, args=["-m", "mcp_server.server"],
    )
    async with Client(transport) as client:
        print("Tools:", [tool.name for tool in await client.list_tools()])
        result = await client.call_tool("get_simulator_status", {})
        print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
