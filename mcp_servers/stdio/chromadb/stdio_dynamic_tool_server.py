import asyncio
import json
import logging
import inspect
import os, sys
import importlib.util

from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# --- Logging Setup ---
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

adk_tools: dict[str, FunctionTool] = {}
TOOL_MODULES_DIR = "tool_modules"
current_script_dir = os.path.dirname(os.path.abspath(__file__))
tool_modules_full_path = os.path.join(current_script_dir, TOOL_MODULES_DIR)

if not os.path.isdir(tool_modules_full_path):
    logging.warning(f"Tool modules directory not found: {tool_modules_full_path}.")
else:
    for filename in os.listdir(tool_modules_full_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(tool_modules_full_path, filename)
            
            try:
                full_module_name = f"{os.path.basename(current_script_dir)}.{module_name}"
                spec = importlib.util.spec_from_file_location(full_module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    logging.info(f"Loaded module: {full_module_name}")

                    for func_name, func_obj in inspect.getmembers(module, inspect.isfunction):
                        if func_name.startswith("_"):
                            continue
                        source_file = inspect.getsourcefile(func_obj)
                        if source_file and os.path.abspath(source_file) == os.path.abspath(module_path):
                            try:
                                adk_tool_instance = FunctionTool(func_obj)
                                adk_tools[adk_tool_instance.name] = adk_tool_instance
                                logging.info(f"Registered tool: {adk_tool_instance.name}")
                            except Exception as e:
                                logging.error(f"Failed to register {func_name}: {e}")
            except Exception as e:
                logging.error(f"Error loading {module_name}: {e}")

server_name = f"{os.path.basename(current_script_dir)}-mcp-server"
app = Server(server_name)

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    mcp_tool_schemas = []
    for tool_name, adk_tool_instance in adk_tools.items():
        try:
            mcp_tool_schemas.append(adk_to_mcp_tool_type(adk_tool_instance))
        except Exception as e:
            logging.error(f"Schema error for {tool_name}: {e}")
    return mcp_tool_schemas

@app.call_tool()
async def call_mcp_tool(tool_name: str, arguments: dict) -> list[mcp_types.TextContent]:
    adk_tool = adk_tools.get(tool_name)
    if adk_tool:
        try:
            response = await adk_tool.run_async(args=arguments, tool_context=None)
            return [mcp_types.TextContent(type="text", text=json.dumps(response, indent=2))]
        except Exception as e:
            return [mcp_types.TextContent(type="text", text=json.dumps({"error": str(e)}))]
    return [mcp_types.TextContent(type="text", text=f"Tool {tool_name} not found")]

async def run_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name=app.name,
            server_version="0.1.0",
            capabilities=app.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={}),
        ))

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        pass
