# Stdio Client

Interactive stdio client that can connect to multiple stdio servers from this repo.

## Run

```bash
python -m mcp_server_client.stdio.agent
```

## Default connected servers

- `mcp_servers/stdio/mac_tts/stdio_dynamic_tool_server.py`
- `mcp_servers/stdio/chromadb/stdio_dynamic_tool_server.py`
- `mcp_servers/stdio/mindmap/stdio_dynamic_tool_server.py`

## Notes

- Uses `sys.executable` so the client and servers share the same Python environment.
- Server list is configured in `ACTIVE_SERVERS` inside `agent.py`.
