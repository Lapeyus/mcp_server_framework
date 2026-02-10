# Stdio Dynamic Tool Server

## 📖 Overview

The **`stdio_dynamic_tool_server.py`** is a **shared, reusable MCP server implementation** used by all stdio-based servers in this framework. Each server (ChromaDB, Mac TTS, Mindmap) uses an identical copy of this file.

## 🎯 Purpose

This server provides a **generic, plugin-based architecture** that:

1. **Automatically discovers** Python functions from a `tool_modules/` directory
2. **Wraps them as ADK tools** using Google's Agent Development Kit
3. **Exposes them via MCP** (Model Context Protocol) over stdio transport
4. **Requires zero configuration** - just add Python functions to `tool_modules/`

## 🏗️ Architecture

```
[Server Directory]
├── stdio_dynamic_tool_server.py    # Generic server (this file)
└── tool_modules/                   # Your tools go here
    ├── __init__.py
    ├── tool1.py                    # Automatically discovered
    └── tool2.py                    # Automatically discovered
```

### How It Works

1. **Server starts** → Scans `tool_modules/` directory
2. **Discovers functions** → Uses Python's `inspect` module
3. **Creates ADK tools** → Wraps each function with `FunctionTool`
4. **Exposes via MCP** → Converts ADK tools to MCP tool schemas
5. **Handles requests** → Routes tool calls to appropriate functions

## 🔧 Key Features

### 1. Dynamic Tool Discovery

No manual registration needed! The server automatically finds and loads all functions from `tool_modules/`:

```python
# tool_modules/my_tool.py
def my_function(param1: str, param2: int) -> dict:
    """This docstring becomes the tool description."""
    return {"result": f"Processed {param1} {param2} times"}
```

### 2. Type-Safe Tool Definitions

Uses Python type hints for automatic schema generation:

```python
def example_tool(
    text: str,           # Required parameter
    count: int = 1,      # Optional with default
    options: dict = {}   # Complex types supported
) -> dict:              # Return type
    """Tool description here."""
    pass
```

### 3. Error Handling

Gracefully handles:
- Missing `tool_modules/` directory
- Import errors in tool modules
- Duplicate tool names
- Tool execution failures

### 4. Logging Support

Optional logging (commented out by default):

```python
# Uncomment to enable logging
import logging
LOG_FILE = "mcp_server.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

## 📝 Creating Tools

### Minimal Example

```python
# tool_modules/hello.py

def say_hello(name: str) -> dict:
    """
    Greet someone by name.
    
    Args:
        name: The person's name
        
    Returns:
        A greeting message
    """
    return {
        "status": "success",
        "message": f"Hello, {name}!"
    }
```

### Advanced Example

```python
# tool_modules/advanced_tool.py

from typing import Optional, List

def process_data(
    input_text: str,
    operation: str = "uppercase",
    repeat: int = 1,
    tags: Optional[List[str]] = None
) -> dict:
    """
    Process text with various operations.
    
    Args:
        input_text: The text to process
        operation: Operation to perform (uppercase, lowercase, reverse)
        repeat: Number of times to repeat the operation
        tags: Optional list of tags to add to result
        
    Returns:
        Processed result with metadata
    """
    result = input_text
    
    for _ in range(repeat):
        if operation == "uppercase":
            result = result.upper()
        elif operation == "lowercase":
            result = result.lower()
        elif operation == "reverse":
            result = result[::-1]
    
    return {
        "status": "success",
        "result": result,
        "operation": operation,
        "repeat_count": repeat,
        "tags": tags or []
    }
```

## 🚀 Usage

### Running the Server

```bash
# From any server directory (chromadb, mac_tts, mindmap)
python stdio_dynamic_tool_server.py
```

### With MCP Client

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/path/to/server/stdio_dynamic_tool_server.py"],
    ),
    errlog=sys.stderr  # See server errors
)
```

### With Claude Desktop

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python3",
      "args": [
        "/absolute/path/to/stdio_dynamic_tool_server.py"
      ]
    }
  }
}
```

## 🔍 How Each Server Uses This

### ChromaDB Server
```
chromadb/
├── stdio_dynamic_tool_server.py    # Shared server
└── tool_modules/
    └── chromadb_tools.py           # ChromaDB-specific functions
```

### Mac TTS Server
```
mac_tts/
├── stdio_dynamic_tool_server.py    # Shared server
└── tool_modules/
    └── tts.py                      # TTS-specific functions
```

### Mindmap Server
```
mindmap/
├── stdio_dynamic_tool_server.py    # Shared server
└── tool_modules/
    └── markmapper.py               # Mindmap-specific functions
```

## 🛠️ Customization

### Server Name

Change the server name on line 94:

```python
app = Server("my-custom-server-name")
```

### Enable Logging

Uncomment lines 3, 20-26, and all `logging.*` calls:

```python
import logging

LOG_FILE = "mcp_server.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

### Custom Tool Loading

Modify the discovery logic (lines 39-89) to:
- Filter specific files
- Add custom validation
- Implement tool namespacing
- Add tool metadata

## 📊 Code Structure

```python
# 1. Imports (lines 1-14)
import asyncio, json, inspect, os, importlib.util
from mcp import types as mcp_types
from google.adk.tools.function_tool import FunctionTool

# 2. Tool Discovery (lines 28-89)
adk_tools: dict[str, FunctionTool] = {}
# Scan tool_modules/ and create FunctionTool instances

# 3. MCP Server Setup (lines 91-140)
app = Server("utility-mcp-server")

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    # Return available tools

@app.call_tool()
async def call_mcp_tool(tool_name: str, arguments: dict):
    # Execute tool and return result

# 4. Server Runner (lines 142-175)
async def run_mcp_stdio_server():
    # Start stdio server

if __name__ == "__main__":
    asyncio.run(run_mcp_stdio_server())
```

## 🐛 Troubleshooting

### Tools Not Discovered

**Problem:** Functions in `tool_modules/` not showing up

**Solutions:**
1. Ensure `__init__.py` exists in `tool_modules/`
2. Check function has type hints
3. Verify function is defined in the module (not imported)
4. Enable logging to see discovery process

### Import Errors

**Problem:** `ModuleNotFoundError` when loading tools

**Solutions:**
1. Install missing dependencies: `pip install -r requirements.txt`
2. Check tool module imports
3. Use absolute imports in tool modules

### Tool Execution Fails

**Problem:** Tool returns error when called

**Solutions:**
1. Check function signature matches arguments
2. Verify return type is JSON-serializable
3. Add error handling in tool function
4. Enable logging to see detailed errors

## 💡 Best Practices

### 1. Tool Function Guidelines

- ✅ Use type hints for all parameters and return types
- ✅ Include comprehensive docstrings
- ✅ Return dictionaries (JSON-serializable)
- ✅ Handle errors gracefully
- ✅ Keep functions focused and single-purpose

### 2. Error Handling

```python
def my_tool(param: str) -> dict:
    """Tool with error handling."""
    try:
        result = process(param)
        return {"status": "success", "result": result}
    except ValueError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Unexpected error: {str(e)}"}
```

### 3. Documentation

```python
def well_documented_tool(param1: str, param2: int = 10) -> dict:
    """
    One-line summary of what the tool does.
    
    Longer description with more details about the tool's
    purpose, behavior, and any important notes.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter (default: 10)
        
    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - result: The processed result
        - metadata: Additional information
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> well_documented_tool("test", 5)
        {"status": "success", "result": "...", "metadata": {...}}
    """
    pass
```

## 🔗 Related Files

- **Template**: `stdio_dynamic_tool_server_template.py` (master copy)
- **Servers using this**:
  - `chromadb/stdio_dynamic_tool_server.py`
  - `mac_tts/stdio_dynamic_tool_server.py`
  - `mindmap/stdio_dynamic_tool_server.py`

## 📚 Further Reading

- [MCP Specification](https://modelcontextprotocol.io/)
- [Google ADK Documentation](https://github.com/google/adk)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Python Inspect Module](https://docs.python.org/3/library/inspect.html)

## 🤝 Contributing

When modifying this shared server:

1. **Test thoroughly** with all three servers
2. **Update all copies** (chromadb, mac_tts, mindmap)
3. **Update this README** if behavior changes
4. **Consider backward compatibility** with existing tools
