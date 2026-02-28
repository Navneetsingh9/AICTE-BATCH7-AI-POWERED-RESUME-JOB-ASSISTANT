# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default model - auto-routes to best free model
DEFAULT_MODEL = "openrouter/free"

# App settings
APP_NAME = "AI Resume & Job Assistant"
APP_ICON = "📄"
APP_LAYOUT = "wide"

# Check if API key is available
def check_api_key():
    if not OPENROUTER_API_KEY:
        return False
    return True