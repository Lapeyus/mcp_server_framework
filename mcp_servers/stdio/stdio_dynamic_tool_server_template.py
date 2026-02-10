import asyncio
import json
import logging
import inspect # for dynamic function discovery
import os # For path manipulation
import importlib.util # For dynamic module loading

# MCP Server Imports
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# No longer importing a single my_functions, will discover from tool_modules


# --- Logging Setup ---
# LOG_FILE = "mcp_server.log"
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )

# --- Prepare the ADK Tools ---
# Dictionary to store ADK FunctionTool instances, keyed by function name
adk_tools: dict[str, FunctionTool] = {}
TOOL_MODULES_DIR = "tool_modules" # Relative to this script's location (mcp_server)
# Construct the full path to the tool_modules directory
# Assuming this script (mac_tts_mcp_server.py) is in the 'mcp_server' directory
current_script_dir = os.path.dirname(os.path.abspath(__file__))
tool_modules_full_path = os.path.join(current_script_dir, TOOL_MODULES_DIR)

# logging.info(f"Dynamically discovering and initializing ADK tools from modules in '{tool_modules_full_path}'...")

if not os.path.isdir(tool_modules_full_path):
    print('.')
    # logging.warning(f"Tool modules directory not found: {tool_modules_full_path}. No dynamic tools will be loaded.")
else:
    for filename in os.listdir(tool_modules_full_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3] # Remove .py extension
            module_path = os.path.join(tool_modules_full_path, filename)
            
            try:
                # Dynamically import the module
                # The module name for importlib should be relative to a package if tool_modules is part of one
                # For simplicity here, we'll use a unique name based on file path.
                # A more robust way might involve adding tool_modules_full_path to sys.path temporarily
                # or using importlib with package context.
                # For mcp_server.tool_modules.module_name:
                full_module_import_name = f"mcp_server.{TOOL_MODULES_DIR}.{module_name}"

                spec = importlib.util.spec_from_file_location(full_module_import_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    # Add to sys.modules BEFORE exec_module to handle circular imports within the module if any
                    # and to make it findable by inspect.getmodule if needed
                    # sys.modules[full_module_import_name] = module # Be cautious with sys.modules modification
                    spec.loader.exec_module(module)
                    # logging.info(f"Successfully imported module: {full_module_import_name}")

                    for func_name, func_obj in inspect.getmembers(module, inspect.isfunction):
                        # Ensure the function is defined in the currently loaded module, not imported into it
                        if func_obj.__module__ == full_module_import_name:
                            try:
                                adk_tool_instance = FunctionTool(func_obj)
                                # Check for duplicate tool names if functions in different modules might lead to same ADK tool name
                                if adk_tool_instance.name in adk_tools:
                                    print('.')
                                    # logging.warning(f"Duplicate ADK tool name '{adk_tool_instance.name}' found. Function '{func_name}' from module '{module_name}' will overwrite existing.")
                                adk_tools[adk_tool_instance.name] = adk_tool_instance
                                print('.')
                                # logging.info(f"ADK tool '{adk_tool_instance.name}' (from function '{func_name}' in '{module_name}.py') initialized.")
                            except Exception as e_tool:
                                print('.')
                                # logging.error(f"Failed to initialize ADK tool for function '{func_name}' in '{module_name}.py': {e_tool}")
                else:
                    print('.')
                    # logging.error(f"Could not create module spec for {module_path}")
            except ImportError as e_import:
                print('.')
                # logging.error(f"Failed to import module '{module_name}' from '{module_path}': {e_import}")
            except Exception as e_module:
                print('.')
                # logging.error(f"Error processing module '{module_name}' from '{module_path}': {e_module}")

# --- MCP Server Setup ---
# logging.info("Creating MCP Server instance...")
print('.')
app = Server("utility-mcp-server")

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """MCP handler to list tools this server exposes."""
    # logging.info("MCP Server: Received list_tools request.")
    print('.')
    mcp_tool_schemas = []
    for tool_name, adk_tool_instance in adk_tools.items():
        try:
            mcp_schema = adk_to_mcp_tool_type(adk_tool_instance)
            mcp_tool_schemas.append(mcp_schema)
            print('.')
            # logging.info(f"MCP Server: Advertising tool: {mcp_schema.name}")
        except Exception as e:
            print('.')
            # logging.error(f"Failed to get MCP schema for ADK tool '{tool_name}': {e}")
    return mcp_tool_schemas

@app.call_tool()
async def call_mcp_tool(tool_name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """MCP handler to execute a tool call requested by an MCP client."""
    # logging.info(f"MCP Server: Received call_tool request for '{tool_name}' with args: {arguments}")
    print('.')

    adk_tool_to_call = adk_tools.get(tool_name)

    if adk_tool_to_call:
        try:
            adk_tool_response = await adk_tool_to_call.run_async(args=arguments,tool_context=None)
            print('.')
            # logging.info(f"MCP Server: ADK tool '{tool_name}' executed. Response: {adk_tool_response}")

            # Serialize the response dict to JSON.
            response_text = json.dumps(adk_tool_response, indent=2)
            # MCP expects a list of mcp_types.TextContent parts
            return [mcp_types.TextContent(type="text", text=response_text)]
        except Exception as e:
            print('.')
            # logging.error(f"MCP Server: Error executing ADK tool '{tool_name}': {e}")
            error_text = json.dumps({"status": "error", "error_message": f"Failed to execute tool '{tool_name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # Handle calls to unknown tools
        # logging.warning(f"MCP Server: Tool '{tool_name}' not found/exposed by this server.")
        error_text = json.dumps({"status": "error", "error_message": f"Tool '{tool_name}' not implemented by this server."})
        return [mcp_types.TextContent(type="text", text=error_text)]

# --- MCP Server Runner ---
async def run_mcp_stdio_server():
    """Runs the MCP server, listening for connections over standard input/output."""
    # Use the stdio_server context manager from the mcp.server.stdio library
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # logging.info("MCP Stdio Server: Starting handshake with client...")
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
    # logging.info("MCP Stdio Server: Run loop finished or client disconnected.")

if __name__ == "__main__":
    # logging.info("Launching Utility MCP Server to expose ADK tools via stdio...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        print('.')
        # logging.info("\nUtility MCP Server (stdio) stopped by user.")
    except Exception as e:
        print('.')
        # logging.error(f"Utility MCP Server (stdio) encountered an error: {e}", exc_info=True)
    finally:
        print('.')
        # logging.info("Utility MCP Server (stdio) process exiting.")
