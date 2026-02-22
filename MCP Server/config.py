"""Configuration settings for MCP Server"""

import os
from utils import get_local_ip

# API Configuration
# Use environment variable or fallback to auto-detected local IP
BACKEND_HOST = os.getenv('BACKEND_HOST', get_local_ip())

# Backward compatibility
LOCAL_IP = BACKEND_HOST
