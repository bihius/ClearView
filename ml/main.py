import logging
import os
from photos import process_image
from photos_watchdog import monitor_folder

logger = logging.getLogger(__name__)

def scan_folder(path, cursor):
    logger.info("Scanning folder: %s", path)
    for root, dirs, files in os.walk(path):
        for file in files:
            process_image(file, cursor)
            

def monitor_folders(paths):
    if not paths:
        logger.error("No folders to monitor")
        return
    else:
        for path in paths:
            monitor_folder(path)