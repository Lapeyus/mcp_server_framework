# Stdio (Standard Input/Output) MCP Client

This client demonstrates how to connect to MCP servers using standard input/output (stdio) transport protocol.

## 📖 Overview

The stdio client connects to MCP servers that communicate via standard input and output streams. This is the most common and versatile transport method for MCP servers, especially for:

- Local tool execution
- Command-line utilities
- Python/Node.js based servers
- Desktop integrations (like Claude Desktop)

## 🎯 What This Client Does

This example client:
- Connects to stdio-based MCP servers (ChromaDB, Mac TTS, Memory, Fetch, etc.)
- Uses local LLM models via Ollama (Qwen3:30b by default)
- Demonstrates multiple server connections (with examples commented out)
- Provides a flexible template for building custom MCP client agents

## 🔧 Configuration

### Connection Parameters

The client shows how to connect to various stdio servers:

#### Active: ChromaDB Server
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/path/to/chromadb_server.py"],
    ),
    errlog=sys.stderr
)
```

#### Commented Examples

**Memory Server (NPX-based):**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='npx',
        args=["-y", "@modelcontextprotocol/server-memory"],
        env={
            "MEMORY_FILE_PATH": "/path/to/memory.json"
        }
    ),
    errlog=sys.stderr
)
```

**Fetch Server (Node.js):**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='node',
        args=["/path/to/fetch-mcp/dist/index.js"],
    )
)
```

**Mac TTS Server:**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/path/to/mac_tts_mcp_server.py"],
    ),
    errlog=sys.stderr
)
```

## 🚀 Usage

### Prerequisites

1. **Install Ollama** (for local LLM):
   ```bash
   # macOS
   brew install ollama
   
   # Start Ollama service
   ollama serve
   ```

2. **Pull the required model**:
   ```bash
   ollama pull qwen3:30b
   # Or use a smaller model:
   # ollama pull gemma3:27b
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   Create a `.env` file in this directory:
   ```env
   # Add any API keys or configuration here
   OPENAI_API_KEY=your_key_here
   ```

### Running the Client

From the repository root:

```bash
python -m mcp_server_client.stdio.agent
```

Or directly:

```bash
cd mcp_server_client/stdio
python agent.py
```

### Example Interactions

With ChromaDB server active:

```
"Search the ADK documentation for information about agents"
"What does the documentation say about tools?"
"Find examples of using the LiteLlm model"
```

## 🔧 Customization

### 1. Change the LLM Model

The client uses LiteLLM with Ollama by default:

```python
root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:30b"),
    # ...
)
```

**Options:**

**Use Gemini (requires API key):**
```python
model='gemini-2.5-pro-preview-05-06'
```

**Use different Ollama model:**
```python
model=LiteLlm(model="ollama/gemma3:27b")
model=LiteLlm(model="ollama_chat/llama3:8b")
```

### 2. Enable Multiple Servers

Uncomment the server configurations you want to use:

```python
tools=[
    MCPToolset(
        connection_params=StdioServerParameters(
            command='npx',
            args=["-y", "@modelcontextprotocol/server-memory"],
            env={"MEMORY_FILE_PATH": "/path/to/memory.json"}
        ),
        errlog=sys.stderr
    ),
    MCPToolset(
        connection_params=StdioServerParameters(
            command='python3',
            args=["/path/to/mac_tts_mcp_server.py"],
        ),
        errlog=sys.stderr
    ),
    # ... add more servers
]
```

### 3. Update File Paths

**Important:** Update the absolute paths in the configuration to match your system:

```python
args=["/Users/YOUR_USERNAME/Documents/playground/mcp_server_framework/mcp_servers/chromadb_server/chromadb_server.py"]
```

Replace with:
```python
args=[os.path.join(os.path.dirname(__file__), "../../mcp_servers/mcp_stdio_chromadb_server/chromadb_server.py")]
```

### 4. Customize Agent Instructions

Modify the agent's behavior:

```python
root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:30b"),
    name='mcp_server_client',
    instruction="""
    You are a helpful assistant with access to:
    - ChromaDB for semantic search
    - Mac TTS for text-to-speech
    - Memory for persistent storage
    
    Help the user by leveraging these tools effectively.
    """,
    tools=[...]
)
```

## 📡 How Stdio Works

Standard input/output (stdio) is a simple IPC (Inter-Process Communication) mechanism:

**Flow:**
1. Client spawns server process with `command` and `args`
2. Client writes JSON-RPC messages to server's stdin
3. Server processes requests and writes responses to stdout
4. Client reads and parses responses
5. Errors are logged to stderr

**Advantages:**
- Simple and reliable
- Works with any language
- No network configuration needed
- Easy to debug (can run server manually)

## 🐛 Troubleshooting

### Server Not Found
```
Error: command not found: python3
```
**Solution:** Ensure the command is in your PATH or use absolute path:
```python
command='/usr/local/bin/python3'
```

### Module Import Errors
```
ModuleNotFoundError: No module named 'google.adk'
```
**Solution:** Install dependencies:
```bash
pip install -r ../../requirements.txt
```

### Ollama Connection Failed
```
Error: Could not connect to Ollama
```
**Solution:** Start Ollama service:
```bash
ollama serve
```

### Path Issues
```
FileNotFoundError: [Errno 2] No such file or directory
```
**Solution:** Update all file paths to absolute paths or use `os.path.join()` for relative paths.

### ChromaDB Server Not Responding
**Solution:** 
1. Test the server independently:
   ```bash
   python ../../mcp_servers/mcp_stdio_chromadb_server/chromadb_server.py
   ```
2. Check server logs in `errlog`

## 🔍 Debugging

Enable error logging to see server stderr:

```python
MCPToolset(
    connection_params=StdioServerParameters(...),
    errlog=sys.stderr  # This shows server errors
)
```

## 📚 Related Files

- **ChromaDB Server**: `../../mcp_servers/mcp_stdio_chromadb_server/chromadb_server.py`
- **Mac TTS Server**: `../../mcp_servers/mcp_stdio_mac_tts_mcp_server/mac_tts_mcp_server.py`
- **Mindmap Server**: `../../mcp_servers/mcp_stdio_mindmap_mcp_server/mcp_server.py`
- **Main README**: `../../README.md`

## 💡 Example Use Cases

### 1. Knowledge Base Assistant
Connect to ChromaDB to search documentation:
```python
instruction="You help users find information in the ADK documentation using semantic search."
```

### 2. Voice Assistant
Combine ChromaDB + Mac TTS:
```python
instruction="Search documentation and read answers aloud using text-to-speech."
```

### 3. Note-Taking Agent
Use Memory server for persistent storage:
```python
instruction="Help users take notes and retrieve them later using the memory server."
```

### 4. Multi-Tool Agent
Enable all servers for comprehensive capabilities:
```python
instruction="You have access to documentation search, text-to-speech, memory, and web fetching. Use these tools to help the user effectively."
```

## 🔗 Learn More

- [MCP Specification](https://modelcontextprotocol.io/)
- [Google ADK Documentation](https://github.com/google/adk)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Ollama Documentation](https://ollama.ai/)
