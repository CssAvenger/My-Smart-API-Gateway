import os
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv

from routes import routes

load_dotenv()

app = routes
