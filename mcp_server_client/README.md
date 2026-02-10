# MCP Server Clients

This directory contains example client implementations for connecting to MCP (Model Context Protocol) servers using different transport protocols.

## 📂 Directory Structure

```
mcp_server_client/
├── README.md                    # This file
├── sse/                         # Server-Sent Events client
│   ├── agent.py
│   └── README.md
├── stdio/                       # Standard Input/Output client
│   ├── agent.py
│   └── README.md
└── streamablehttp/              # Streamable HTTP client
    ├── agent.py
    └── README.md
```

## 🎯 Overview

Each client demonstrates how to:
- Connect to MCP servers using a specific transport protocol
- Use Google's ADK (Agent Development Kit) to create AI agents
- Integrate MCP tools into agent workflows
- Implement security best practices (tool filtering, access control)

## 🚀 Quick Start

### Choose Your Transport

| Transport | Use When | Example |
|-----------|----------|---------|
| **[Stdio](stdio/)** | Local tools, CLI utilities, Python/Node servers | ChromaDB, Mac TTS, Mindmap |
| **[SSE](sse/)** | Real-time updates, browser apps, one-way streaming | File system monitoring, live data |
| **[Streamable HTTP](streamablehttp/)** | Web APIs, microservices, cloud deployments | RESTful services, distributed systems |

### Installation

1. **Install dependencies** (from repository root):
   ```bash
   pip install -r requirements.txt
   ```

2. **Choose a client** and follow its README:
   - [Stdio Client](stdio/README.md) - Most versatile, works with local servers
   - [SSE Client](sse/README.md) - Best for real-time, one-way streaming
   - [Streamable HTTP Client](streamablehttp/README.md) - Best for web deployments

## 📖 Client Guides

### 1. Stdio Client ([Full Guide](stdio/README.md))

**Best for:** Local MCP servers (ChromaDB, Mac TTS, Mindmap, etc.)

**Quick Start:**
```bash
# Run the ChromaDB client example
python -m mcp_server_client.stdio.agent
```

**Features:**
- Connects to local MCP servers via stdin/stdout
- Uses Ollama for local LLM inference
- Multiple server support (ChromaDB, Memory, Fetch, TTS)
- No network configuration needed

**Example Configuration:**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/path/to/server.py"],
    ),
    errlog=sys.stderr
)
```

---

### 2. SSE Client ([Full Guide](sse/README.md))

**Best for:** Real-time data streaming, browser-compatible applications

**Quick Start:**
```bash
# Start the SSE server first
cd ../mcp_servers/mcp_sse_server
python filesystem_server.py

# Then run the client
python -m mcp_server_client.sse.agent
```

**Features:**
- HTTP-based Server-Sent Events transport
- Real-time, one-way communication (server → client)
- Read-only filesystem access
- Browser-native support

**Example Configuration:**
```python
MCPToolset(
    connection_params=SseServerParams(
        url='http://localhost:3000/sse',
        headers={'Accept': 'text/event-stream'},
    )
)
```

---

### 3. Streamable HTTP Client ([Full Guide](streamablehttp/README.md))

**Best for:** Web APIs, microservices, cloud deployments

**Quick Start:**
```bash
# Start the Streamable HTTP server first
cd ../mcp_servers/mcp_streamablehttp_agent
python server.py

# Then run the client
python -m mcp_server_client.streamablehttp.agent
```

**Features:**
- RESTful HTTP-based transport
- Bidirectional streaming
- Authentication support (headers, tokens)
- Load balancer and proxy compatible

**Example Configuration:**
```python
MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
    )
)
```

## 🔧 Common Patterns

### Tool Filtering

All clients demonstrate security best practices with tool filtering:

**Allowlist Approach (Recommended):**
```python
tool_filter=[
    'read_file',
    'list_directory',
    'search_files',
    # Only allow specific safe tools
]
```

**Blocklist Approach:**
```python
tool_filter=lambda tool, ctx=None: tool.name not in [
    'write_file',
    'delete_file',
    'execute_command',
    # Block dangerous operations
]
```

### Model Selection

**Use Gemini (Cloud):**
```python
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    # or
    model='gemini-2.5-pro-preview-05-06',
)
```

**Use Ollama (Local):**
```python
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:30b"),
    # or
    model=LiteLlm(model="ollama/gemma3:27b"),
)
```

### Multiple Server Connections

Connect to multiple MCP servers in one agent:

```python
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='multi_tool_agent',
    instruction="You have access to multiple tools...",
    tools=[
        # ChromaDB for semantic search
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/path/to/chromadb_server.py"],
            )
        ),
        # Mac TTS for speech
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/path/to/mac_tts_server.py"],
            )
        ),
        # Web fetch via HTTP
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:3000/fetch',
            )
        ),
    ],
)
```

## 🔒 Security Best Practices

1. **Always use tool filtering** to restrict dangerous operations
2. **Limit directory access** using `_allowed_path` or server-side controls
3. **Use HTTPS** for network-based transports in production
4. **Implement authentication** for HTTP-based transports
5. **Log errors** using `errlog=sys.stderr` for debugging
6. **Validate inputs** before passing to MCP tools
7. **Use environment variables** for sensitive configuration

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Install all dependencies
pip install -r ../requirements.txt
```

**Server Not Found:**
```bash
# Ensure server is running first
cd ../mcp_servers/[server_name]
python server.py
```

**Ollama Not Available:**
```bash
# Install and start Ollama
brew install ollama
ollama serve
ollama pull qwen3:30b
```

**Path Issues:**
```python
# Use absolute paths or os.path.join
import os
server_path = os.path.join(
    os.path.dirname(__file__),
    "../../mcp_servers/server.py"
)
```

## 📊 Transport Comparison

| Feature | Stdio | SSE | Streamable HTTP |
|---------|-------|-----|-----------------|
| **Network Required** | ❌ No | ✅ Yes | ✅ Yes |
| **Bidirectional** | ✅ Yes | ❌ No | ✅ Yes |
| **Browser Support** | ❌ No | ✅ Yes | ✅ Yes |
| **Setup Complexity** | ⭐ Low | ⭐⭐ Medium | ⭐⭐ Medium |
| **Authentication** | N/A | ✅ Headers | ✅ Headers |
| **Cloud Deployment** | ❌ No | ✅ Yes | ✅ Yes |
| **Best For** | Local tools | Real-time updates | Web APIs |

## 💡 Example Use Cases

### Local Development Assistant
```python
# Use stdio client with ChromaDB + Mac TTS
# Search docs, read answers aloud
```

### Real-time Monitoring Dashboard
```python
# Use SSE client for live file system updates
# Stream changes to browser
```

### Distributed Microservices
```python
# Use Streamable HTTP client
# Connect services across network
```

### Multi-Modal Agent
```python
# Combine all transports
# Stdio for local tools
# HTTP for remote services
# SSE for real-time updates
```

## 🔗 Related Documentation

- **Main README**: [../README.md](../README.md)
- **MCP Servers**: [../mcp_servers/](../mcp_servers/)
- **MCP Specification**: https://modelcontextprotocol.io/
- **Google ADK**: https://github.com/google/adk

## 📝 Creating Your Own Client

To create a custom client:

1. **Choose a transport** based on your needs
2. **Copy an existing client** as a template
3. **Update connection parameters** for your server
4. **Customize the agent**:
   - Model selection
   - Instructions
   - Tool filtering
5. **Test thoroughly** with your MCP server

### Minimal Example

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='my_agent',
    instruction="Help the user with...",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/path/to/my_server.py"],
            )
        )
    ],
)
```

## 🤝 Contributing

When adding new clients:
1. Create a new directory with descriptive name
2. Include `agent.py` with the client implementation
3. Add comprehensive `README.md` documentation
4. Update this main README with your client
5. Add examples and use cases

## 📄 License

See [LICENSE](../LICENSE) file in the repository root.
