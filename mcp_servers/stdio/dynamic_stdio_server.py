from __future__ import annotations

import asyncio
import importlib.util
import inspect
import json
import logging
import os
import sys
from pathlib import Path

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _load_tools_from_directory(tool_modules_dir: Path) -> dict[str, FunctionTool]:
    adk_tools: dict[str, FunctionTool] = {}

    if not tool_modules_dir.is_dir():
        logging.warning("Tool modules directory not found: %s", tool_modules_dir)
        return adk_tools

    for module_path in sorted(tool_modules_dir.glob("*.py")):
        if module_path.name == "__init__.py":
            continue

        module_name = module_path.stem
        import_name = f"{tool_modules_dir.parent.name}.{module_name}"
        spec = importlib.util.spec_from_file_location(import_name, module_path)

        if spec is None or spec.loader is None:
            logging.error("Could not create module spec for %s", module_path)
            continue

        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logging.info("Loaded module: %s", import_name)
        except Exception as exc:
            logging.error("Error loading module %s: %s", module_name, exc)
            continue

        for func_name, func_obj in inspect.getmembers(module, inspect.isfunction):
            if func_name.startswith("_"):
                continue
            if inspect.getsourcefile(func_obj) != str(module_path):
                continue

            try:
                adk_tool = FunctionTool(func_obj)
                adk_tools[adk_tool.name] = adk_tool
                logging.info("Registered tool: %s", adk_tool.name)
            except Exception as exc:
                logging.error("Failed to register %s: %s", func_name, exc)

    return adk_tools


def create_stdio_server(server_dir: Path) -> tuple[Server, dict[str, FunctionTool]]:
    adk_tools = _load_tools_from_directory(server_dir / "tool_modules")
    app = Server(f"{server_dir.name}-mcp-server")

    @app.list_tools()
    async def list_mcp_tools() -> list[mcp_types.Tool]:
        mcp_tools: list[mcp_types.Tool] = []
        for tool_name, adk_tool in adk_tools.items():
            try:
                mcp_tools.append(adk_to_mcp_tool_type(adk_tool))
            except Exception as exc:
                logging.error("Schema error for %s: %s", tool_name, exc)
        return mcp_tools

    @app.call_tool()
    async def call_mcp_tool(
        tool_name: str, arguments: dict
    ) -> list[mcp_types.TextContent]:
        adk_tool = adk_tools.get(tool_name)
        if adk_tool is None:
            return [
                mcp_types.TextContent(type="text", text=f"Tool {tool_name} not found")
            ]

        try:
            response = await adk_tool.run_async(args=arguments, tool_context=None)
            return [
                mcp_types.TextContent(type="text", text=json.dumps(response, indent=2))
            ]
        except Exception as exc:
            return [
                mcp_types.TextContent(
                    type="text", text=json.dumps({"error": str(exc)})
                )
            ]

    return app, adk_tools


async def run_stdio_server(server_dir: str | Path) -> None:
    resolved_server_dir = Path(server_dir).resolve()
    app, _ = create_stdio_server(resolved_server_dir)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main(server_dir: str | Path | None = None) -> None:
    target_dir = Path(server_dir or os.getcwd()).resolve()
    try:
        asyncio.run(run_stdio_server(target_dir))
    except KeyboardInterrupt:
        pass
