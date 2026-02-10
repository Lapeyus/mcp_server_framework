# Stdio MCP Servers

This directory contains MCP servers that use the **stdio (Standard Input/Output)** transport protocol.

## 📖 Overview

Stdio servers communicate via standard input and output streams, making them ideal for:
- Local tool execution
- Command-line utilities
- Desktop application integrations (like Claude Desktop)
- Python/Node.js based servers
- No network configuration required

## 🗂️ Available Servers

### 1. ChromaDB Server (`chromadb/`)

**Purpose:** Vector database operations for semantic search and embeddings

**Features:**
- Store and retrieve embeddings
- Semantic search capabilities
- Document storage and retrieval
- Collection management

**Use Cases:**
- Documentation search
- Knowledge base queries
- Semantic similarity matching
- RAG (Retrieval Augmented Generation) applications

**Quick Start:**
```bash
cd chromadb
python chromadb_server.py
```

---

### 2. Mac TTS Server (`mac_tts/`)

**Purpose:** Native macOS text-to-speech synthesis

**Features:**
- Convert text to speech using macOS voices
- Save audio to files (AIFF, M4A, WAV)
- Multiple voice options
- Direct playback or file output

**Use Cases:**
- Accessibility features
- Voice notifications
- Audio content generation
- Reading assistance

**Quick Start:**
```bash
cd mac_tts
python tool_modules/tts.py  # Test directly
# Or run as MCP server:
python mac_tts_mcp_server.py
```

---

### 3. Mindmap Server (`mindmap/`)

**Purpose:** Convert markdown to interactive HTML mind maps

**Features:**
- Markdown to Markmap conversion
- Interactive HTML visualization
- Customizable styling
- Auto-formatting for non-markdown content

**Use Cases:**
- Project planning visualization
- Note organization
- Brainstorming sessions
- Documentation structure

**Quick Start:**
```bash
cd mindmap
python tool_modules/markmapper.py  # Generate sample
# Or run as MCP server:
python mcp_server.py
```

## 🚀 Using Stdio Servers

### Method 1: Direct Execution (Testing)

Run the server directly to test functionality:

```bash
cd [server_name]
python [server_script].py
```

### Method 2: With MCP Client

Use with the stdio client from `mcp_server_client/stdio/`:

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=["/absolute/path/to/server.py"],
    ),
    errlog=sys.stderr
)
```

### Method 3: Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chromadb": {
      "command": "python3",
      "args": [
        "/absolute/path/to/mcp_servers/stdio/chromadb/chromadb_server.py"
      ]
    },
    "mac-tts": {
      "command": "python3",
      "args": [
        "/absolute/path/to/mcp_servers/stdio/mac_tts/mac_tts_mcp_server.py"
      ]
    },
    "mindmap": {
      "command": "python3",
      "args": [
        "/absolute/path/to/mcp_servers/stdio/mindmap/mcp_server.py"
      ]
    }
  }
}
```

## 🔧 Common Configuration

All stdio servers in this directory follow a similar pattern:

### Server Structure
```
[server_name]/
├── mcp_server.py          # Main server entry point
├── tool_modules/          # Tool implementations
│   ├── __init__.py
│   └── [tool].py         # Individual tool functions
└── README.md             # Server-specific documentation
```

### Dynamic Tool Loading

Servers automatically discover and load tools from `tool_modules/`:

```python
# Tools are automatically discovered from tool_modules/
# No manual registration needed!
```

### Error Logging

Enable error logging for debugging:

```python
MCPToolset(
    connection_params=StdioServerParameters(...),
    errlog=sys.stderr  # See server errors
)
```

## 🛠️ Development

### Adding a New Stdio Server

1. **Create server directory:**
   ```bash
   mkdir my_new_server
   cd my_new_server
   ```

2. **Create tool_modules directory:**
   ```bash
   mkdir tool_modules
   touch tool_modules/__init__.py
   ```

3. **Add your tool functions:**
   ```python
   # tool_modules/my_tool.py
   def my_function(param1: str, param2: int) -> dict:
       """Tool description for MCP."""
       # Your implementation
       return {"result": "success"}
   ```

4. **Copy server template:**
   ```bash
   cp ../chromadb/chromadb_server.py ./mcp_server.py
   # Update server name in the file
   ```

5. **Test your server:**
   ```bash
   python mcp_server.py
   ```

### Tool Function Requirements

For automatic discovery, tool functions must:
- Be defined in `tool_modules/*.py`
- Have type hints for parameters
- Include a docstring (used as tool description)
- Return a dictionary or serializable object

Example:
```python
def example_tool(text: str, count: int = 1) -> dict:
    """
    This is an example tool that processes text.
    
    Args:
        text: The text to process
        count: Number of times to repeat (default: 1)
    
    Returns:
        Dictionary with processed result
    """
    return {
        "status": "success",
        "result": text * count
    }
```

## 🐛 Troubleshooting

### Server Won't Start
```
Error: ModuleNotFoundError
```
**Solution:** Install dependencies:
```bash
pip install -r ../../../requirements.txt
```

### Tools Not Discovered
```
Warning: No tools found
```
**Solution:** 
- Ensure tools are in `tool_modules/` directory
- Check that functions have proper type hints
- Verify `__init__.py` exists in `tool_modules/`

### Permission Denied
```
Error: Permission denied
```
**Solution:** Make server executable:
```bash
chmod +x mcp_server.py
```

### Import Errors
```
Error: Cannot import module
```
**Solution:** Set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/mcp_server_framework:$PYTHONPATH
```

## 📊 Server Comparison

| Server | Primary Use | Complexity | Dependencies |
|--------|-------------|------------|--------------|
| **ChromaDB** | Semantic search | ⭐⭐⭐ | chromadb, embeddings |
| **Mac TTS** | Text-to-speech | ⭐ | macOS only |
| **Mindmap** | Visualization | ⭐⭐ | None (uses CDN) |

## 🔗 Related Documentation

- **Stdio Client**: `../../mcp_server_client/stdio/README.md`
- **Main README**: `../../README.md`
- **MCP Specification**: https://modelcontextprotocol.io/

## 📝 Best Practices

1. **Use absolute paths** in configuration
2. **Enable error logging** during development
3. **Test tools independently** before MCP integration
4. **Document your tools** with clear docstrings
5. **Handle errors gracefully** in tool functions
6. **Use type hints** for automatic schema generation
7. **Keep tools focused** on single responsibilities

## 💡 Example Multi-Server Setup

Combine multiple stdio servers in one agent:

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='multi_tool_assistant',
    instruction="""
    You have access to:
    - ChromaDB for searching documentation
    - Mac TTS for reading text aloud
    - Mindmap for visualizing ideas
    
    Use these tools to help the user effectively.
    """,
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
        MCPToolset(
            connection_params=StdioServerParameters(
                command='python3',
                args=["/path/to/mindmap/mcp_server.py"],
            )
        ),
    ],
)
```
