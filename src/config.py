"""
Central configuration for the Offline AI Agent.

This file stores all configurable values used throughout the project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# -------------------------
# Model Configuration
# -------------------------

# Local Ollama model to use
MODEL = "qwen3:4b"

# Maximum number of tool-calling iterations
MAX_STEPS = 6

# -------------------------
# Project Paths
# -------------------------

# Root folder of the project
ROOT_DIR = Path(__file__).resolve().parent.parent

# Folder where the agent is allowed to create/read files
SANDBOX_DIR = ROOT_DIR / "sandbox"

# Optional custom Ollama server
OLLAMA_HOST = os.getenv("OLLAMA_HOST")