# SSE (Server-Sent Events) MCP Client

This client demonstrates how to connect to an MCP server using Server-Sent Events (SSE) transport protocol.

## 📖 Overview

The SSE client connects to MCP servers that expose their functionality over HTTP using Server-Sent Events for real-time, one-way communication from server to client. This is ideal for:

- Real-time data streaming
- Long-lived connections
- Browser-compatible implementations
- Scenarios where WebSockets are not available

## 🎯 What This Client Does

This example client:
- Connects to an SSE-based MCP server running on `http://localhost:3000/sse`
- Provides read-only filesystem access tools
- Uses Google's ADK (Agent Development Kit) with Gemini 2.0 Flash model
- Filters tools to only allow safe read operations (no write/edit/delete)

## 🔧 Configuration

### Connection Parameters

```python
MCPToolset(
    connection_params=SseServerParams(
        url='http://localhost:3000/sse',
        headers={'Accept': 'text/event-stream'},
    ),
    tool_filter=[
        'read_file',
        'read_multiple_files',
        'list_directory',
        'directory_tree',
        'search_files',
        'get_file_info',
        'list_allowed_directories',
    ],
)
```

### Available Tools (Filtered)

The client only exposes these safe, read-only tools:
- `read_file` - Read contents of a single file
- `read_multiple_files` - Read multiple files at once
- `list_directory` - List directory contents
- `directory_tree` - Get directory tree structure
- `search_files` - Search for files
- `get_file_info` - Get file metadata
- `list_allowed_directories` - List accessible directories

## 🚀 Usage

### Prerequisites

1. **Start the SSE MCP Server** (from the repository root):
   ```bash
   cd mcp_servers/mcp_sse_server
   python filesystem_server.py
   ```
   The server should be running on `http://localhost:3000/sse`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Client

From the repository root:

```bash
python -m mcp_server_client.sse.agent
```

Or directly:

```bash
cd mcp_server_client/sse
python agent.py
```

### Example Interactions

Once running, you can ask the agent questions like:

```
"List all files in the current directory"
"Read the contents of README.md"
"Search for Python files in this directory"
"Show me the directory tree"
```

## 🔒 Security Features

This client implements security best practices:

- **Read-only access**: Write operations are filtered out
- **Directory restrictions**: Only allowed directories are accessible
- **Tool filtering**: Dangerous operations are explicitly excluded

### Commented Tool Filter Alternative

The code includes an alternative lambda-based filter approach:

```python
tool_filter=lambda tool, ctx=None: tool.name not in [
    'write_file',
    'edit_file',
    'create_directory',
    'move_file',
]
```

You can uncomment this to use dynamic filtering instead of an explicit allowlist.

## 🛠️ Customization

### Change the Model

Replace the model in `agent.py`:

```python
root_agent = LlmAgent(
    model='gemini-2.0-flash',  # Change to your preferred model
    # ...
)
```

### Modify Allowed Directory

The client restricts access to its own directory by default:

```python
_allowed_path = os.path.dirname(os.path.abspath(__file__))
```

Update this to allow access to different directories.

### Add More Tools

To enable write operations (use with caution):

```python
tool_filter=[
    'read_file',
    'write_file',      # Add this
    'edit_file',       # Add this
    'list_directory',
    # ... other tools
]
```

## 📡 How SSE Works

Server-Sent Events (SSE) is a standard describing how servers can initiate data transmission towards clients once an initial client connection has been established.

**Flow:**
1. Client opens HTTP connection to SSE endpoint
2. Server keeps connection open
3. Server sends events as they occur
4. Client receives and processes events in real-time

**Advantages:**
- Simple HTTP-based protocol
- Automatic reconnection
- Browser native support
- Efficient for one-way communication

## 🐛 Troubleshooting

### Connection Refused
- Ensure the SSE server is running on `http://localhost:3000/sse`
- Check firewall settings

### No Tools Available
- Verify the server is exposing tools correctly
- Check the tool filter configuration

### Permission Errors
- Verify the `_allowed_path` includes the directories you're trying to access
- Check file system permissions

## 📚 Related Files

- **Server**: `mcp_servers/mcp_sse_server/filesystem_server.py`
- **Main README**: `../../README.md`

## 🔗 Learn More

- [MCP Specification](https://modelcontextprotocol.io/)
- [Google ADK Documentation](https://github.com/google/adk)
- [Server-Sent Events MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
