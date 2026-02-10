# MCP Servers

This directory contains MCP (Model Context Protocol) server implementations organized by transport type.

## 📂 Directory Structure

```
mcp_servers/
├── README.md                    # This file
├── stdio/                       # Standard I/O transport servers
│   ├── README.md
│   ├── chromadb/               # Vector database server
│   ├── mac_tts/                # Text-to-speech server
│   └── mindmap/                # Mind mapping server
├── sse/                        # Server-Sent Events transport servers
│   ├── README.md
│   └── filesystem/             # File system access server
└── streamablehttp/             # HTTP streaming transport servers
    ├── README.md
    └── agent/                  # Agent server
```

## 🎯 Quick Overview

### By Transport Type

| Transport | Servers | Best For |
|-----------|---------|----------|
| **[Stdio](stdio/)** | ChromaDB, Mac TTS, Mindmap | Local tools, CLI utilities, desktop apps |
| **[SSE](sse/)** | Filesystem | Real-time updates, browser apps, monitoring |
| **[Streamable HTTP](streamablehttp/)** | Agent | Web APIs, microservices, cloud deployments |

### By Functionality

| Server | Transport | Purpose | Use Cases |
|--------|-----------|---------|-----------|
| **[ChromaDB](stdio/chromadb/)** | Stdio | Vector database | Semantic search, RAG, embeddings |
| **[Mac TTS](stdio/mac_tts/)** | Stdio | Text-to-speech | Voice output, accessibility |
| **[Mindmap](stdio/mindmap/)** | Stdio | Visualization | Planning, brainstorming, docs |
| **[Filesystem](sse/filesystem/)** | SSE | File access | Browsing, monitoring, exploration |
| **[Agent](streamablehttp/agent/)** | HTTP | Agent services | Web APIs, distributed systems |

## 🚀 Quick Start

### Choose Your Server

1. **For local development and tools:**
   - Use **[Stdio servers](stdio/)** (ChromaDB, Mac TTS, Mindmap)
   - No network configuration needed
   - Easy to debug and test

2. **For real-time browser applications:**
   - Use **[SSE servers](sse/)** (Filesystem)
   - Native browser support
   - One-way streaming from server

3. **For web APIs and cloud deployments:**
   - Use **[Streamable HTTP servers](streamablehttp/)** (Agent)
   - RESTful and scalable
   - Authentication and load balancing ready

### Installation

From the repository root:

```bash
# Install all dependencies
pip install -r requirements.txt
```

### Running Servers

Each server can be run independently:

```bash
# Stdio servers
cd stdio/chromadb && python chromadb_server.py
cd stdio/mac_tts && python mac_tts_mcp_server.py
cd stdio/mindmap && python mcp_server.py

# SSE servers
cd sse/filesystem && python filesystem_server.py

# Streamable HTTP servers
cd streamablehttp/agent && python server.py
```

## 📖 Transport Guides

### [Stdio Servers](stdio/README.md)

**Standard Input/Output transport**

- ✅ Local execution
- ✅ Simple debugging
- ✅ No network setup
- ❌ Not network-accessible

**Servers:**
- ChromaDB - Vector database operations
- Mac TTS - Text-to-speech synthesis
- Mindmap - Markdown to mind maps

**Quick Example:**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/path/to/server.py"],
    )
)
```

---

### [SSE Servers](sse/README.md)

**Server-Sent Events transport**

- ✅ Real-time streaming
- ✅ Browser native support
- ✅ HTTP-based
- ❌ One-way only (server → client)

**Servers:**
- Filesystem - Read-only file access

**Quick Example:**
```python
MCPToolset(
    connection_params=SseServerParams(
        url='http://localhost:3000/sse',
    )
)
```

---

### [Streamable HTTP Servers](streamablehttp/README.md)

**HTTP Streaming transport**

- ✅ Bidirectional streaming
- ✅ RESTful and scalable
- ✅ Authentication support
- ✅ Cloud-native

**Servers:**
- Agent - General-purpose agent server

**Quick Example:**
```python
MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
    )
)
```

## 🔧 Configuration Patterns

### Single Server

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='my_agent',
    instruction="Help the user...",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/path/to/chromadb/chromadb_server.py"],
            )
        )
    ],
)
```

### Multiple Servers (Same Transport)

```python
tools=[
    MCPToolset(
        connection_params=StdioServerParameters(
            command='python3',
            args=["/path/to/chromadb/chromadb_server.py"],
        )
    ),
    MCPToolset(
        connection_params=StdioServerParameters(
            command='python3',
            args=["/path/to/mac_tts/mac_tts_mcp_server.py"],
        )
    ),
]
```

### Multiple Servers (Mixed Transports)

```python
tools=[
    # Local ChromaDB via stdio
    MCPToolset(
        connection_params=StdioServerParameters(
            command='python3',
            args=["/path/to/chromadb/chromadb_server.py"],
        )
    ),
    # Remote filesystem via SSE
    MCPToolset(
        connection_params=SseServerParams(
            url='http://localhost:3000/sse',
        )
    ),
    # Web API via HTTP
    MCPToolset(
        connection_params=StreamableHTTPServerParams(
            url='https://api.example.com/mcp',
        )
    ),
]
```

## 🛠️ Development

### Adding a New Server

1. **Choose transport type** (stdio, sse, or streamablehttp)
2. **Create server directory:**
   ```bash
   cd [transport_type]
   mkdir my_new_server
   cd my_new_server
   ```

3. **Follow transport-specific template:**
   - [Stdio template](stdio/README.md#adding-a-new-stdio-server)
   - [SSE template](sse/README.md#adding-a-new-sse-server)
   - [HTTP template](streamablehttp/README.md)

4. **Test your server:**
   ```bash
   python server.py
   ```

5. **Document your server:**
   - Create README.md in server directory
   - Update transport type README
   - Update this main README

### Server Structure Best Practices

**Stdio servers:**
```
my_server/
├── mcp_server.py          # Main entry point
├── tool_modules/          # Tool implementations
│   ├── __init__.py
│   └── my_tool.py
└── README.md
```

**SSE/HTTP servers:**
```
my_server/
├── server.py              # Flask/FastAPI app
├── handlers/              # Request handlers
├── models/                # Data models
└── README.md
```

## 📊 Transport Comparison

| Feature | Stdio | SSE | Streamable HTTP |
|---------|-------|-----|-----------------|
| **Network** | ❌ Local only | ✅ Yes | ✅ Yes |
| **Bidirectional** | ✅ Yes | ❌ No | ✅ Yes |
| **Browser Support** | ❌ No | ✅ Native | ✅ Yes |
| **Setup Complexity** | ⭐ Low | ⭐⭐ Medium | ⭐⭐ Medium |
| **Authentication** | N/A | ✅ HTTP headers | ✅ HTTP headers |
| **Load Balancing** | N/A | ✅ Yes | ✅ Yes |
| **Cloud Deployment** | ❌ No | ✅ Yes | ✅ Yes |
| **Debugging** | ⭐⭐⭐ Easy | ⭐⭐ Medium | ⭐⭐ Medium |
| **Best For** | Local tools | Real-time updates | Web APIs |

## 🔒 Security Best Practices

### All Servers

1. **Validate all inputs** before processing
2. **Handle errors gracefully** with proper error messages
3. **Log security events** for auditing
4. **Keep dependencies updated** regularly

### Network Servers (SSE, HTTP)

5. **Use HTTPS in production** for encryption
6. **Implement authentication** (tokens, API keys)
7. **Add rate limiting** to prevent abuse
8. **Enable CORS** only for trusted origins
9. **Validate file paths** to prevent traversal attacks
10. **Use environment variables** for secrets

## 🐛 Common Issues

### Server Won't Start

```bash
# Check dependencies
pip install -r ../../requirements.txt

# Check port availability
lsof -i :3000

# Check Python version
python --version  # Should be 3.8+
```

### Import Errors

```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/mcp_server_framework:$PYTHONPATH

# Or use absolute imports
```

### Connection Refused

```bash
# Ensure server is running
ps aux | grep python

# Check firewall
# macOS: System Preferences > Security & Privacy > Firewall
```

## 💡 Example Use Cases

### 1. Local Development Assistant

**Servers:** ChromaDB (stdio) + Mac TTS (stdio)

```python
# Search documentation, read answers aloud
tools=[
    MCPToolset(connection_params=StdioServerParameters(...)),  # ChromaDB
    MCPToolset(connection_params=StdioServerParameters(...)),  # Mac TTS
]
```

### 2. Real-time File Monitor

**Servers:** Filesystem (SSE)

```python
# Monitor files in browser
tools=[
    MCPToolset(connection_params=SseServerParams(...)),
]
```

### 3. Distributed Microservices

**Servers:** Agent (HTTP) + ChromaDB (stdio)

```python
# Local DB + Remote API
tools=[
    MCPToolset(connection_params=StdioServerParameters(...)),  # Local
    MCPToolset(connection_params=StreamableHTTPServerParams(...)),  # Remote
]
```

### 4. Multi-Modal Agent

**Servers:** All types

```python
# Combine all capabilities
tools=[
    MCPToolset(connection_params=StdioServerParameters(...)),  # ChromaDB
    MCPToolset(connection_params=StdioServerParameters(...)),  # Mac TTS
    MCPToolset(connection_params=StdioServerParameters(...)),  # Mindmap
    MCPToolset(connection_params=SseServerParams(...)),        # Filesystem
    MCPToolset(connection_params=StreamableHTTPServerParams(...)),  # Agent
]
```

## 🔗 Related Documentation

- **MCP Clients**: `../mcp_server_client/README.md`
- **Main README**: `../README.md`
- **MCP Specification**: https://modelcontextprotocol.io/
- **Google ADK**: https://github.com/google/adk

## 📝 Contributing

When adding new servers:

1. Choose appropriate transport type
2. Follow existing patterns and structure
3. Include comprehensive README
4. Add examples and use cases
5. Update all relevant documentation
6. Test thoroughly before committing

## 📄 License

See [LICENSE](../LICENSE) file in the repository root.
