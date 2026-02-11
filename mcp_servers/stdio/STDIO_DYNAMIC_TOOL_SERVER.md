# Dynamic Stdio Server

The stdio server runtime is centralized in:

- `mcp_servers/stdio/dynamic_stdio_server.py`

Each stdio server folder contains a tiny wrapper (`stdio_dynamic_tool_server.py`) that calls the shared runtime with its own directory.

## Why this exists

- Removes duplicated server bootstrap code across `chromadb`, `mac_tts`, and `mindmap`.
- Keeps tool loading behavior identical across servers.
- Makes future fixes in one place.

## Tool Discovery Rules

- Files: all `tool_modules/*.py`, excluding `__init__.py`
- Functions: public functions only (names not starting with `_`)
- Function source must belong to that module file

## Minimal wrapper example

```python
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
STDIO_ROOT = CURRENT_DIR.parent

if str(STDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(STDIO_ROOT))

from dynamic_stdio_server import main

if __name__ == "__main__":
    main(CURRENT_DIR)
```
