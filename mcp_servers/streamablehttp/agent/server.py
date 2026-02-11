# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pathlib import Path
import sys

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Filesystem Server", host="localhost", port=3000)


@mcp.tool(description="Read contents of a file")
def read_file(filepath: str) -> str:
    """Read and return the contents of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool(description="List contents of a directory")
def list_directory(dirpath: str) -> list:
    """List all files and directories in the given directory."""
    return os.listdir(dirpath)


@mcp.tool(description="Get current working directory")
def get_cwd() -> str:
    """Return the current working directory."""
    return str(Path.cwd())


def main() -> None:
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        print("Thank you for using the Filesystem MCP Server!")


if __name__ == "__main__":
    main()
