# MCP Server Clients

Client examples for connecting to servers in this repository.

## Structure

```text
mcp_server_client/
├── stdio/
├── sse/
└── streamablehttp/
```

## Run

From repository root:

```bash
python -m mcp_server_client.stdio.agent
python -m mcp_server_client.sse.agent
python -m mcp_server_client.streamablehttp.agent
```

## Notes

- The stdio client can connect to multiple local stdio servers in one session.
- The SSE and Streamable HTTP clients default to `localhost:3000`.
