# MCP Servers

This directory contains MCP server implementations grouped by transport.

## Structure

```text
mcp_servers/
├── stdio/
│   ├── dynamic_stdio_server.py
│   ├── chromadb/
│   ├── mac_tts/
│   └── mindmap/
├── sse/
│   └── filesystem/
└── streamablehttp/
    └── agent/
```

## Run

From repository root:

```bash
# stdio
python mcp_servers/stdio/chromadb/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mac_tts/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mindmap/stdio_dynamic_tool_server.py

# sse
python mcp_servers/sse/filesystem/filesystem_server.py

# streamable-http
python mcp_servers/streamablehttp/agent/server.py
```

## Transport Docs

- `mcp_servers/stdio/README.md`
- `mcp_servers/sse/README.md`
- `mcp_servers/streamablehttp/README.md`
