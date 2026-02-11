# MCP Server Framework

A Python monorepo with MCP server and client examples using three transports:
- `stdio`
- `sse`
- `streamable-http`

## Repository Layout

```text
mcp_server_framework/
├── mcp_servers/
│   ├── stdio/
│   ├── sse/
│   └── streamablehttp/
├── mcp_server_client/
│   ├── stdio/
│   ├── sse/
│   └── streamablehttp/
├── requirements.txt
└── PRE_PUSH_CHECKLIST.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Servers

### Stdio servers

```bash
python mcp_servers/stdio/chromadb/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mac_tts/stdio_dynamic_tool_server.py
python mcp_servers/stdio/mindmap/stdio_dynamic_tool_server.py
```

### SSE server

```bash
python mcp_servers/sse/filesystem/filesystem_server.py
# endpoint: http://localhost:3000/sse
```

### Streamable HTTP server

```bash
python mcp_servers/streamablehttp/agent/server.py
# endpoint: http://localhost:3000/mcp
```

`mcp_servers/streamablehttp/agent/filesystem_server.py` is kept as a compatibility alias.

## Run Clients

```bash
python -m mcp_server_client.stdio.agent
python -m mcp_server_client.sse.agent
python -m mcp_server_client.streamablehttp.agent
```

## Notes

- Stdio servers share a common runtime in `mcp_servers/stdio/dynamic_stdio_server.py`.
- Tool discovery for stdio servers is automatic from each server's `tool_modules/` folder.
- For push readiness, follow `PRE_PUSH_CHECKLIST.md`.
