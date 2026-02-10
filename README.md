# MCP Server Framework

This repository provides a framework and examples for building Model Context Protocol (MCP) servers and clients using Python and Google's Agent Development Kit (ADK).

It demonstrates how to expose local tools and services (like ChromaDB, Text-to-Speech, Mind Mapping) as MCP servers that can be consumed by MCP-compliant clients (like Claude, IDEs, or custom agents).

## ✨ Features

This framework includes ready-to-use MCP servers for:

- **🗄️ ChromaDB Integration** - Vector database operations for semantic search and embeddings
- **🔊 Mac Text-to-Speech** - Native macOS speech synthesis for audio output
- **🧠 Mind Mapping** - Convert markdown to interactive HTML mind maps with Markmap
- **📡 SSE Transport** - Server-Sent Events for real-time streaming
- **🌐 HTTP Streaming** - Streamable HTTP for web-based integrations


## 📂 Repository Structure

- **`mcp_servers/`**: MCP server implementations organized by transport type.
  - **`stdio/`**: Standard I/O transport servers (local execution)
    - **`chromadb/`**: Vector database for semantic search and embeddings
    - **`mac_tts/`**: Native macOS text-to-speech synthesis
    - **`mindmap/`**: Markdown to interactive HTML mind maps
  - **`sse/`**: Server-Sent Events transport servers (real-time streaming)
    - **`filesystem/`**: Read-only filesystem access
  - **`streamablehttp/`**: HTTP streaming transport servers (web APIs)
    - **`agent/`**: General-purpose agent server

- **`mcp_server_client/`**: Client implementations for connecting to MCP servers.
  - **`sse/`**: Client for SSE-based servers
  - **`stdio/`**: Client for stdio-based servers
  - **`streamablehttp/`**: Client for HTTP streaming servers

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
  ],
  "env": {
    "PYTHONPATH": "/absolute/path/to/mcp_server_framework"
  }
}
```
**Note:** `PYTHONPATH` is set to the project root to ensure the server script can import shared modules and dependencies from within the framework.

### Running the Mindmap Server (Stdio)

Convert markdown content into interactive HTML mind maps using Markmap.

**1. Direct Test (Generate a sample mindmap):**
```bash
python mcp_servers/mcp_stdio_mindmap_mcp_server/tool_modules/markmapper.py
# This will create test_markmap_corrected.html - open it in a browser
```

**2. Configure in Claude Desktop:**
Add to your `claude_desktop_config.json`:
```json
"mindmap": {
  "command": "python3",
  "args": [
    "/absolute/path/to/mcp_server_framework/mcp_servers/mcp_stdio_mindmap_mcp_server/mcp_server.py"
  ],
  "env": {
    "PYTHONPATH": "/absolute/path/to/mcp_server_framework"
  }
}
```

**3. Example Usage:**
Once configured, you can ask Claude to create mind maps from markdown:
```markdown
# Project Planning
- Phase 1: Research
  - Market Analysis
  - Competitor Study
- Phase 2: Development
  - Backend API
  - Frontend UI
- Phase 3: Launch
  - Testing
  - Deployment
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