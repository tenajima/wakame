import os
import logging

name = "wakame"

PID = os.getpid()
LOGGING_FORMAT = f"[{PID}] %(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
logging.addLevelName(logging.ERROR, "Error")
logging.addLevelName(logging.INFO, "Info")
logging.addLevelName(logging.WARNING, "Warning")
