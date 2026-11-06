"""Проверка опубликованного MCP-интерфейса шаблона."""
import asyncio

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from mcp_server.server import create_server
from mcp_server.settings import Settings
from mcp_server.simulator import SimulatorClient


def test_mcp_exposes_status_and_refuses_unimplemented_calculation() -> None:
    async def scenario() -> None:
        simulator = SimulatorClient(Settings(
            simulator_name="not-configured", simulator_model_path=None,
        ))
        async with Client(create_server(simulator)) as client:
            names = {tool.name for tool in await client.list_tools()}
            assert names == {"get_simulator_status", "run_simulation"}
            status = await client.call_tool("get_simulator_status", {})
            assert status.structured_content["status"] == "not_configured"
            with pytest.raises(ToolError, match="Подключите API"):
                await client.call_tool("run_simulation", {
                    "case_id": "test", "parameters": {"pressure_bar": 100.0},
                })

    asyncio.run(scenario())
