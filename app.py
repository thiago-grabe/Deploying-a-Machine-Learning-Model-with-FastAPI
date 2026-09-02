"""
Vercel entrypoint shim.

Vercel's zero-config FastAPI preset looks for a top-level `app` in a root
entrypoint file; the real application lives in starter/main.py, which also
configures logging and loads the model artifacts on import.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "starter"))

from main import app  # noqa: E402,F401
