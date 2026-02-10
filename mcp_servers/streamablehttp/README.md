# Streamable HTTP MCP Servers

This directory contains MCP servers that use the **Streamable HTTP** transport protocol.

## 📖 Overview

Streamable HTTP servers communicate via HTTP with streaming capabilities, making them ideal for:
- Web-based applications and APIs
- RESTful service integrations
- Microservices architectures
- Cloud-native deployments
- Bidirectional streaming over HTTP
- Load-balanced environments

## 🗂️ Available Servers

### Agent Server (`agent/`)

**Purpose:** Provide MCP agent functionality via HTTP streaming

**Features:**
- HTTP-based request/response with streaming
- RESTful API endpoints
- Bidirectional communication
- Standard HTTP middleware support
- Authentication and authorization ready

**Use Cases:**
- Web application backends
- API gateways
- Microservice communication
- Cloud deployments
- Multi-tenant systems

**Quick Start:**
```bash
cd agent
python server.py  # Adjust based on actual server file
# Server starts on http://localhost:3000/mcp
```

## 🚀 Using Streamable HTTP Servers

### Method 1: Direct HTTP Access

Test the server with curl:

```bash
# Start the server
cd agent
python server.py

# List available tools
curl -X POST http://localhost:3000/mcp/list_tools \
  -H "Content-Type: application/json"

# Call a tool
curl -X POST http://localhost:3000/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "example_tool",
    "arguments": {"param": "value"}
  }'
```

### Method 2: With MCP Client

Use with the Streamable HTTP client from `mcp_server_client/streamablehttp/`:

```python
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
    )
)
```

### Method 3: With Authentication

Add authentication headers:

```python
MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url='http://localhost:3000/mcp',
        headers={
            'Authorization': 'Bearer YOUR_TOKEN',
            'X-API-Key': 'your-api-key',
        }
    )
)
```

## 🔧 Server Configuration

### Basic Setup

```python
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/mcp/list_tools', methods=['POST'])
def list_tools():
    tools = [
        {"name": "tool1", "description": "First tool"},
        {"name": "tool2", "description": "Second tool"},
    ]
    return Response(
        json.dumps(tools),
        mimetype='application/json'
    )

@app.route('/mcp/call_tool', methods=['POST'])
def call_tool():
    data = request.json
    tool_name = data.get('tool_name')
    arguments = data.get('arguments', {})
    
    # Process tool call
    result = process_tool(tool_name, arguments)
    
    return Response(
        json.dumps(result),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
```

### Streaming Response

For streaming responses:

```python
@app.route('/mcp/stream', methods=['POST'])
def stream_response():
    def generate():
        for chunk in process_streaming_data():
            yield json.dumps(chunk) + '\n'
    
    return Response(
        generate(),
        mimetype='application/x-ndjson',  # Newline-delimited JSON
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )
```

### CORS Configuration

Enable CORS for browser access:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/mcp/*": {
        "origins": ["http://localhost:3000", "https://yourapp.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 🌐 Deployment

### Local Development

```python
if __name__ == '__main__':
    app.run(
        host='localhost',
        port=3000,
        debug=True  # Enable debug mode
    )
```

### Production with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:3000 server:app
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "server:app"]
```

```bash
# Build and run
docker build -t mcp-server .
docker run -p 3000:3000 mcp-server
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        ports:
        - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
spec:
  selector:
    app: mcp-server
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

## 🔒 Security

### 1. Authentication Middleware

```python
from functools import wraps
from flask import request, abort
import jwt

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            abort(401, 'No token provided')
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = payload
        except jwt.InvalidTokenError:
            abort(401, 'Invalid token')
        
        return f(*args, **kwargs)
    return decorated

@app.route('/mcp/call_tool', methods=['POST'])
@require_auth
def call_tool():
    # Access user info via request.user
    pass
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/mcp/call_tool', methods=['POST'])
@limiter.limit("10 per minute")
def call_tool():
    pass
```

### 3. Input Validation

```python
from marshmallow import Schema, fields, ValidationError

class ToolCallSchema(Schema):
    tool_name = fields.Str(required=True)
    arguments = fields.Dict(required=True)

@app.route('/mcp/call_tool', methods=['POST'])
def call_tool():
    schema = ToolCallSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return Response(
            json.dumps({"error": err.messages}),
            status=400,
            mimetype='application/json'
        )
    
    # Process validated data
    pass
```

### 4. HTTPS/TLS

```python
# Production: Use reverse proxy (Nginx, Traefik)
# Or SSL context:
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=('cert.pem', 'key.pem')
    )
```

## 🛠️ Load Balancing

### Nginx Configuration

```nginx
upstream mcp_backend {
    least_conn;  # Load balancing method
    server localhost:3001;
    server localhost:3002;
    server localhost:3003;
}

server {
    listen 80;
    server_name api.example.com;

    location /mcp {
        proxy_pass http://mcp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # For streaming
        proxy_buffering off;
        proxy_read_timeout 300s;
    }
}
```

### Health Checks

```python
@app.route('/health', methods=['GET'])
def health_check():
    return Response(
        json.dumps({"status": "healthy"}),
        mimetype='application/json'
    )

@app.route('/ready', methods=['GET'])
def readiness_check():
    # Check dependencies (DB, etc.)
    if check_dependencies():
        return Response(
            json.dumps({"status": "ready"}),
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({"status": "not ready"}),
            status=503,
            mimetype='application/json'
        )
```

## 🐛 Troubleshooting

### Connection Timeout

```python
# Increase timeout
app.config['TIMEOUT'] = 300  # 5 minutes

# Or in Gunicorn:
# gunicorn --timeout 300 server:app
```

### CORS Issues

```bash
# Install Flask-CORS
pip install flask-cors

# Enable for all routes
from flask_cors import CORS
CORS(app)
```

### Port Already in Use

```bash
# Find and kill process
lsof -ti:3000 | xargs kill

# Or use different port
python server.py --port 3001
```

### Memory Issues

```python
# Use streaming for large responses
def generate_large_response():
    for chunk in get_data_chunks():
        yield json.dumps(chunk) + '\n'

@app.route('/large-data')
def large_data():
    return Response(generate_large_response())
```

## 📊 Monitoring

### Logging

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('mcp_server.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/mcp/call_tool', methods=['POST'])
def call_tool():
    app.logger.info(f"Tool called: {request.json.get('tool_name')}")
    # ...
```

### Metrics

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Metrics available at /metrics endpoint
```

## 💡 Example Use Cases

### 1. API Gateway Pattern

```python
# Aggregate multiple services
@app.route('/mcp/aggregate', methods=['POST'])
def aggregate():
    results = {
        'service1': call_service1(),
        'service2': call_service2(),
    }
    return Response(json.dumps(results))
```

### 2. Webhook Handler

```python
@app.route('/mcp/webhook', methods=['POST'])
def webhook():
    event = request.json
    process_webhook(event)
    return Response(json.dumps({"status": "received"}))
```

### 3. Async Task Queue

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@app.route('/mcp/async-task', methods=['POST'])
def async_task():
    task = process_task.delay(request.json)
    return Response(json.dumps({"task_id": task.id}))

@celery.task
def process_task(data):
    # Long-running task
    pass
```

## 🔗 Related Documentation

- **Streamable HTTP Client**: `../../mcp_server_client/streamablehttp/README.md`
- **Main README**: `../../README.md`
- **Flask Documentation**: https://flask.palletsprojects.com/
- **MCP Specification**: https://modelcontextprotocol.io/

## 📝 Best Practices

1. **Use proper HTTP status codes** (200, 400, 401, 500, etc.)
2. **Implement authentication** for production
3. **Enable CORS** only for trusted origins
4. **Use HTTPS** in production
5. **Implement rate limiting** to prevent abuse
6. **Add health check endpoints** for monitoring
7. **Use streaming** for large responses
8. **Log all requests** for debugging
9. **Validate all inputs** before processing
10. **Handle errors gracefully** with proper error responses
