import logging
import os

log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()

# Configure logging for FastAPI and Uvicorn
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Get root logger
logger = logging.getLogger("webscraper")  # Custom logger name
logger.setLevel(log_level)

# Apply logging to Uvicorn
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers  # Attach handlers
uvicorn_logger.setLevel(log_level)

