"""Фабрика локального MCP-сервера проекта."""

import argparse
from typing import Any

from fastmcp import FastMCP

from .settings import Settings
from .simulator import SimulatorClient


def create_server(client: SimulatorClient | None = None) -> FastMCP:
    """Создать сервер с внедряемым клиентом симулятора."""
    simulator = client or SimulatorClient(Settings.from_env())
    server = FastMCP("engineering-simulator")

    @server.tool()
    def get_simulator_status() -> dict[str, str | None]:
        """Проверить, настроено ли подключение к инженерному ПО."""
        return simulator.status()

    @server.tool()
    def run_simulation(
        case_id: str,
        parameters: dict[str, float],
    ) -> dict[str, Any]:
        """Запустить расчётный сценарий с параметрами в единицах проекта."""
        return simulator.run_case(case_id=case_id, parameters=parameters)

    return server


mcp = create_server()


def main() -> None:
    """Запустить stdio или loopback HTTP для локальной проверки."""
    parser = argparse.ArgumentParser(description="Локальный MCP-сервер проекта")
    parser.add_argument("--http", action="store_true")
    args = parser.parse_args()
    if args.http:
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
