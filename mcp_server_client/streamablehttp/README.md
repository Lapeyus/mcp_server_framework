# Streamable HTTP MCP Client

This client demonstrates how to connect to an MCP server using Streamable HTTP transport protocol.

## 📖 Overview

The Streamable HTTP client connects to MCP servers that expose their functionality over HTTP with streaming capabilities. This transport method is ideal for:

- Web-based applications
- RESTful API integrations
- Scenarios requiring HTTP middleware (auth, load balancing, etc.)
- Cloud-native deployments
- Bidirectional streaming over HTTP

## 🎯 What This Client Does

This example client:
- Connects to a Streamable HTTP MCP server running on `http://localhost:3000/mcp`
- Provides read-only filesystem access tools
- Uses Google's ADK (Agent Development Kit) with Gemini 2.0 Flash model
- Filters tools to only allow safe read operations (no write/edit/delete)

## 🔧 Configuration

### Connection Parameters

```python
MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
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

1. **Start the Streamable HTTP MCP Server** (from the repository root):
   ```bash
   cd mcp_servers/mcp_streamablehttp_agent
   python server.py  # Adjust based on actual server file
   ```
   The server should be running on `http://localhost:3000/mcp`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Client

From the repository root:

```bash
python -m mcp_server_client.streamablehttp.agent
```

Or directly:

```bash
cd mcp_server_client/streamablehttp
python agent.py
```

### Example Interactions

Once running, you can ask the agent questions like:

```
"List all files in the current directory"
"Read the contents of README.md"
"Search for Python files in this directory"
"Show me the directory tree"
"Get information about the agent.py file"
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
    # Options:
    # model='gemini-2.5-pro-preview-05-06'
    # model='gemini-1.5-flash'
)
```

### Modify Server URL

Update the connection URL to point to your server:

```python
connection_params=StreamableHTTPServerParams(
    url='http://your-server.com:8080/mcp',
)
```

### Add Authentication

If your server requires authentication:

```python
connection_params=StreamableHTTPServerParams(
    url='http://localhost:3000/mcp',
    headers={
        'Authorization': 'Bearer YOUR_TOKEN_HERE',
        'X-API-Key': 'your-api-key',
    }
)
```

### Modify Allowed Directory

The client restricts access to its own directory by default:

```python
_allowed_path = os.path.dirname(os.path.abspath(__file__))
```

Update this to allow access to different directories:

```python
_allowed_path = '/path/to/your/allowed/directory'
```

### Add More Tools

To enable write operations (use with caution):

```python
tool_filter=[
    'read_file',
    'write_file',           # Add this
    'edit_file',            # Add this
    'create_directory',     # Add this
    'list_directory',
    'search_files',
    # ... other tools
]
```

Or remove the filter entirely to allow all tools:

```python
MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
    ),
    # No tool_filter = all tools allowed
)
```

## 📡 How Streamable HTTP Works

Streamable HTTP is an HTTP-based transport that supports streaming responses:

**Flow:**
1. Client sends HTTP POST request to server endpoint
2. Server processes request and opens streaming response
3. Server streams data chunks as they become available
4. Client receives and processes chunks in real-time
5. Connection closes when streaming completes

**Advantages:**
- Standard HTTP protocol (works with existing infrastructure)
- Supports authentication and middleware
- Can use HTTPS for encryption
- Compatible with load balancers and proxies
- Bidirectional streaming capabilities
- RESTful and web-friendly

**Differences from SSE:**
- More flexible than SSE (bidirectional)
- Can use standard HTTP methods (POST, GET, etc.)
- Better suited for request-response patterns with streaming

## 🌐 Deployment Considerations

### Local Development
```python
url='http://localhost:3000/mcp'
```

### Production Deployment
```python
url='https://api.yourcompany.com/mcp'
```

### Behind a Proxy
Ensure your proxy supports streaming:
```nginx
# Nginx example
location /mcp {
    proxy_pass http://backend:3000;
    proxy_buffering off;  # Important for streaming
    proxy_read_timeout 300s;
}
```

### Load Balancing
Use sticky sessions if the server maintains state:
```python
connection_params=StreamableHTTPServerParams(
    url='https://mcp-cluster.com/mcp',
    headers={
        'X-Session-ID': 'unique-session-id',
    }
)
```

## 🐛 Troubleshooting

### Connection Refused
```
Error: Connection refused to http://localhost:3000/mcp
```
**Solution:** 
- Ensure the Streamable HTTP server is running
- Check the URL and port number
- Verify firewall settings

### Timeout Errors
```
Error: Request timeout
```
**Solution:**
- Increase timeout in server configuration
- Check network connectivity
- Verify server is responsive

### No Tools Available
```
Warning: No tools available from server
```
**Solution:**
- Verify the server is exposing tools correctly
- Check the tool filter configuration
- Test server endpoint directly:
  ```bash
  curl -X POST http://localhost:3000/mcp/list_tools
  ```

### Permission Errors
```
Error: Access denied to directory
```
**Solution:**
- Verify the `_allowed_path` includes the directories you're trying to access
- Check file system permissions on the server
- Review server-side access controls

### SSL/TLS Errors
```
Error: SSL certificate verification failed
```
**Solution:**
- Use valid SSL certificates in production
- For development, you might need to disable verification (not recommended):
  ```python
  # Not recommended for production!
  import ssl
  ssl._create_default_https_context = ssl._create_unverified_context
  ```

## 🔍 Debugging

### Enable Verbose Logging

Add logging to see detailed communication:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Server Directly

Use curl to test the server:

```bash
# List available tools
curl -X POST http://localhost:3000/mcp/list_tools

# Call a tool
curl -X POST http://localhost:3000/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "list_directory", "arguments": {"path": "."}}'
```

## 📚 Related Files

- **Server**: `../../mcp_servers/mcp_streamablehttp_agent/`
- **SSE Client**: `../sse/README.md` (alternative transport)
- **Stdio Client**: `../stdio/README.md` (alternative transport)
- **Main README**: `../../README.md`

## 💡 Example Use Cases

### 1. Web Application Integration
Integrate MCP tools into a web application:
```python
# In your web backend
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

mcp_tools = MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='https://mcp.yourapp.com/api',
        headers={'Authorization': f'Bearer {user_token}'}
    )
)
```

### 2. Microservices Architecture
Connect multiple services via MCP:
```python
# Service A connects to Service B's MCP endpoint
connection_params=StreamableHTTPServerParams(
    url='http://service-b:3000/mcp',
    headers={'X-Service-Name': 'service-a'}
)
```

### 3. Cloud Deployment
Deploy MCP servers in the cloud:
```python
# Connect to cloud-hosted MCP server
connection_params=StreamableHTTPServerParams(
    url='https://mcp-server.cloud.google.com/mcp',
    headers={
        'Authorization': f'Bearer {gcp_token}',
        'X-Project-ID': 'my-project'
    }
)
```

### 4. API Gateway Pattern
Use MCP behind an API gateway:
```python
connection_params=StreamableHTTPServerParams(
    url='https://api-gateway.com/mcp/v1',
    headers={
        'X-API-Key': api_key,
        'X-Client-Version': '1.0.0'
    }
)
```

## 🔗 Learn More

- [MCP Specification](https://modelcontextprotocol.io/)
- [Google ADK Documentation](https://github.com/google/adk)
- [HTTP Streaming Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
- [RESTful API Design](https://restfulapi.net/)

## 🆚 Comparison with Other Transports

| Feature | Streamable HTTP | SSE | Stdio |
|---------|----------------|-----|-------|
| **Network** | Yes | Yes | No (local only) |
| **Bidirectional** | Yes | No (server→client only) | Yes |
| **Browser Support** | Yes | Yes | No |
| **Complexity** | Medium | Low | Low |
| **Use Case** | Web APIs, microservices | Real-time updates | Local tools, CLI |
| **Authentication** | Easy (HTTP headers) | Easy (HTTP headers) | N/A |
| **Deployment** | Cloud-friendly | Cloud-friendly | Local only |

Choose **Streamable HTTP** when you need:
- Web-based deployments
- Bidirectional streaming
- Standard HTTP infrastructure
- Authentication and authorization
- Load balancing and proxying
