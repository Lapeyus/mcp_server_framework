from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
STDIO_ROOT = CURRENT_DIR.parent

if str(STDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(STDIO_ROOT))

from dynamic_stdio_server import main


if __name__ == "__main__":
    main(CURRENT_DIR)
