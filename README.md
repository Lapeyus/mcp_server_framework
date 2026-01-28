# MCP Server Framework

This repository provides a framework and examples for building Model Context Protocol (MCP) servers and clients using Python and Google's Agent Development Kit (ADK).

It demonstrates how to expose local tools and services (like ChromaDB, Text-to-Speech) as MCP servers that can be consumed by MCP-compliant clients (like Claude, IDEs, or custom agents).

## 📂 Repository Structure

- **`mcp_servers/`**: Contains various MCP server implementations.
  - **`mcp_sse_server/`**: An MCP server using Server-Sent Events (SSE) for transport.
  - **`mcp_stdio_chromadb_server/`**: Exposes ChromaDB operations via standard input/output (stdio).
  - **`mcp_stdio_mac_tts_mcp_server/`**: Exposes Mac's native Text-to-Speech via stdio.
  - **`mcp_streamablehttp_agent/`**: A server implementation using streamable HTTP.

- **`mcp_server_client/`**: Contains client implementations to connect to the above servers.
  - **`sse/`**: Client for the SSE server.
  - **`stdio/`**: Client for stdio-based servers.
  - **`streamablehttp/`**: Client for the streamable HTTP agent.

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Lapeyus/mcp_server_framework.git
    cd mcp_server_framework
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage Examples

### Running a Stdio Server (e.g., ChromaDB)

You can run a stdio server directly or configure it in your MCP client configuration (e.g., in a `claude_desktop_config.json`).

```bash
# Run directly (mostly for testing interaction)
python mcp_servers/mcp_stdio_chromadb_server/chromadb_server.py
```

### Running the SSE Server

1.  Navigate to the server directory:
    ```bash
    cd mcp_servers/mcp_sse_server
    ```

2.  Run the server:
    ```bash
    python filesystem_server.py
    ```

### Running the Mac TTS Server (Stdio)

Expose your Mac's native text-to-speech engine as an MCP tool.

**1. Direct Test (Verify audio works):**
```bash
python mcp_servers/mcp_stdio_mac_tts_mcp_server/tool_modules/tts.py
# You should hear "Hello from Python..."
```

**2. Configure in Claude Desktop:**
Add to your `claude_desktop_config.json`:
```json
"mac-tts": {
  "command": "python3",
  "args": [
    "/absolute/path/to/mcp_server_framework/mcp_servers/mcp_stdio_mac_tts_mcp_server/mac_tts_mcp_server.py"
  ]
}
```

### Using a Client

To test a server with included clients:

```bash
# Example: Running the stdio client
python -m mcp_server_client.stdio.agent
```

## 🧩 Modifying & Adding Tools

The servers are designed to dynamically load tools from a `tool_modules` directory within each server's folder. 

1.  Create a new Python file in `mcp_servers/<server_name>/tool_modules/`.
2.  Define regular Python functions.
3.  The framework will automatically discover these functions, wrap them as ADK tools, and expose them via MCP.

## 📄 License

[License Information Here]