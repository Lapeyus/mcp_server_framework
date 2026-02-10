# SSE MCP Servers

This directory contains MCP servers that use the **SSE (Server-Sent Events)** transport protocol.

## 📖 Overview

SSE servers communicate via HTTP Server-Sent Events, making them ideal for:
- Real-time data streaming
- Browser-compatible applications
- One-way server-to-client communication
- Long-lived HTTP connections
- Event-driven architectures

## 🗂️ Available Servers

### Filesystem Server (`filesystem/`)

**Purpose:** Provide read-only filesystem access via SSE

**Features:**
- Read file contents
- List directory contents
- Search for files
- Get file metadata
- Directory tree visualization
- Read multiple files at once

**Use Cases:**
- File browsing applications
- Documentation viewers
- Code exploration tools
- Real-time file monitoring
- Web-based file managers

**Quick Start:**
```bash
cd filesystem
python filesystem_server.py
# Server starts on http://localhost:3000/sse
```

**Available Tools:**
- `read_file` - Read a single file
- `read_multiple_files` - Read multiple files
- `list_directory` - List directory contents
- `directory_tree` - Get directory structure
- `search_files` - Search for files
- `get_file_info` - Get file metadata
- `list_allowed_directories` - List accessible paths

## 🚀 Using SSE Servers

### Method 1: Direct HTTP Access

Test the server with curl:

```bash
# Start the server
cd filesystem
python filesystem_server.py

# In another terminal, connect via SSE
curl -N -H "Accept: text/event-stream" http://localhost:3000/sse
```

### Method 2: With MCP Client

Use with the SSE client from `mcp_server_client/sse/`:

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseServerParams

MCPToolset(
    connection_params=SseServerParams(
        url='http://localhost:3000/sse',
        headers={'Accept': 'text/event-stream'},
    )
)
```

### Method 3: Browser Integration

SSE is natively supported in browsers:

```javascript
const eventSource = new EventSource('http://localhost:3000/sse');

eventSource.onmessage = (event) => {
  console.log('Received:', event.data);
};

eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
};
```

## 🔧 Server Configuration

### Port and Host

Default configuration:
```python
# Server runs on:
host = 'localhost'
port = 3000
endpoint = '/sse'
```

To change:
```python
# In filesystem_server.py
app.run(host='0.0.0.0', port=8080)  # Accessible from network
```

### Allowed Directories

Configure which directories are accessible:

```python
# In filesystem_server.py
_allowed_path = os.path.dirname(os.path.abspath(__file__))
# Or specify custom paths:
_allowed_paths = [
    '/path/to/docs',
    '/path/to/projects',
]
```

### CORS Configuration

For browser access from different origins:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

## 🛠️ Development

### Adding a New SSE Server

1. **Create server directory:**
   ```bash
   mkdir my_sse_server
   cd my_sse_server
   ```

2. **Create Flask app with SSE:**
   ```python
   from flask import Flask, Response
   import json
   
   app = Flask(__name__)
   
   @app.route('/sse')
   def sse_endpoint():
       def event_stream():
           # Your SSE logic here
           data = {"message": "Hello from SSE"}
           yield f"data: {json.dumps(data)}\n\n"
       
       return Response(
           event_stream(),
           mimetype='text/event-stream',
           headers={
               'Cache-Control': 'no-cache',
               'X-Accel-Buffering': 'no'
           }
       )
   
   if __name__ == '__main__':
       app.run(port=3000)
   ```

3. **Test your server:**
   ```bash
   python my_sse_server.py
   curl -N -H "Accept: text/event-stream" http://localhost:3000/sse
   ```

### SSE Message Format

Standard SSE message format:

```
data: {"type": "message", "content": "Hello"}\n\n
```

With event type:
```
event: custom_event\n
data: {"key": "value"}\n\n
```

With ID (for reconnection):
```
id: 123\n
data: {"message": "data"}\n\n
```

## 🌐 Network Configuration

### Local Development
```python
app.run(host='localhost', port=3000)
# Accessible at: http://localhost:3000/sse
```

### Network Access
```python
app.run(host='0.0.0.0', port=3000)
# Accessible at: http://YOUR_IP:3000/sse
```

### Behind Nginx

Nginx configuration for SSE:

```nginx
location /sse {
    proxy_pass http://localhost:3000;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
    proxy_buffering off;
    proxy_cache off;
}
```

### HTTPS/SSL

For production, use HTTPS:

```python
# Using SSL context
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=('cert.pem', 'key.pem')
    )
```

## 🐛 Troubleshooting

### Connection Refused
```
Error: Connection refused
```
**Solution:** 
- Ensure server is running: `python filesystem_server.py`
- Check port is not in use: `lsof -i :3000`
- Verify firewall settings

### CORS Errors (Browser)
```
Error: CORS policy blocked
```
**Solution:** Install and enable Flask-CORS:
```bash
pip install flask-cors
```
```python
from flask_cors import CORS
CORS(app)
```

### Buffering Issues
```
Events not received in real-time
```
**Solution:** Disable buffering:
```python
Response(
    event_stream(),
    headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'  # Disable nginx buffering
    }
)
```

### Port Already in Use
```
Error: Address already in use
```
**Solution:** 
- Kill existing process: `lsof -ti:3000 | xargs kill`
- Or use different port: `app.run(port=3001)`

## 📊 SSE vs Other Transports

| Feature | SSE | Stdio | Streamable HTTP |
|---------|-----|-------|-----------------|
| **Direction** | Server → Client | Bidirectional | Bidirectional |
| **Protocol** | HTTP | Process IPC | HTTP |
| **Browser Support** | ✅ Native | ❌ No | ✅ Yes |
| **Reconnection** | ✅ Automatic | N/A | Manual |
| **Complexity** | ⭐⭐ Medium | ⭐ Low | ⭐⭐ Medium |
| **Best For** | Real-time updates | Local tools | Web APIs |

## 🔒 Security Considerations

### 1. Path Traversal Protection

Always validate paths:

```python
import os

def is_safe_path(path, allowed_dir):
    real_path = os.path.realpath(path)
    real_allowed = os.path.realpath(allowed_dir)
    return real_path.startswith(real_allowed)
```

### 2. Authentication

Add authentication for production:

```python
from functools import wraps
from flask import request, abort

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/sse')
@require_auth
def sse_endpoint():
    # ...
```

### 3. Rate Limiting

Prevent abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/sse')
@limiter.limit("10 per minute")
def sse_endpoint():
    # ...
```

## 💡 Example Use Cases

### 1. Real-time File Monitoring

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def file_monitor_stream():
    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            yield f"data: {json.dumps({'file': event.src_path})}\n\n"
    
    observer = Observer()
    observer.schedule(Handler(), path='.')
    observer.start()
```

### 2. Log Streaming

```python
def log_stream():
    with open('app.log', 'r') as f:
        f.seek(0, 2)  # Go to end
        while True:
            line = f.readline()
            if line:
                yield f"data: {json.dumps({'log': line})}\n\n"
            time.sleep(0.1)
```

### 3. Progress Updates

```python
def progress_stream():
    for i in range(100):
        time.sleep(0.1)
        yield f"data: {json.dumps({'progress': i})}\n\n"
    yield f"data: {json.dumps({'status': 'complete'})}\n\n"
```

## 🔗 Related Documentation

- **SSE Client**: `../../mcp_server_client/sse/README.md`
- **Main README**: `../../README.md`
- **MDN SSE Guide**: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- **MCP Specification**: https://modelcontextprotocol.io/

## 📝 Best Practices

1. **Always set proper headers** (`Cache-Control`, `X-Accel-Buffering`)
2. **Implement reconnection logic** with event IDs
3. **Validate all file paths** to prevent directory traversal
4. **Use HTTPS in production** for security
5. **Implement rate limiting** to prevent abuse
6. **Handle client disconnections** gracefully
7. **Keep messages small** for better performance
8. **Use event types** for different message categories
