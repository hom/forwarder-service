import os
import uvicorn
from app.config import HOST, PORT, LOG_LEVEL

if __name__ == "__main__":
    reload = os.getenv("RELOAD", "false").lower() == "true"
    uvicorn.run("app.main:app", host=HOST, port=PORT, log_level=LOG_LEVEL, reload=reload)
