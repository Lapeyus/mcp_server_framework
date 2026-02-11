# Stdio MCP Servers

Stdio servers in this repo share one runtime and load tools dynamically from `tool_modules/`.

## Shared Runtime

- Runtime file: `mcp_servers/stdio/dynamic_stdio_server.py`
- Per-server entrypoint: `stdio_dynamic_tool_server.py`
- Behavior: load all non-private functions from `tool_modules/*.py` and expose them as MCP tools.

## Available Stdio Servers

- `mcp_servers/stdio/chromadb/stdio_dynamic_tool_server.py`
- `mcp_servers/stdio/mac_tts/stdio_dynamic_tool_server.py`
- `mcp_servers/stdio/mindmap/stdio_dynamic_tool_server.py`

## Run

From repository root:

```bash
python mcp_servers/stdio/chromadb/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mac_tts/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mindmap/stdio_dynamic_tool_server.py
```

## Add a New Stdio Server

1. Create a folder under `mcp_servers/stdio/`.
2. Add `tool_modules/` with one or more tool files.
3. Add `stdio_dynamic_tool_server.py` using the template at:
   - `mcp_servers/stdio/stdio_dynamic_tool_server_template.py`
