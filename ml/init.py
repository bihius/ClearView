import logging
import os
from ml.photos import process_image

logger = logging.getLogger(__name__)

def scan_folder(images_path, cursor):
    logger.info("Scanning folder: %s", images_path)
    for root, dirs, files in os.walk(images_path):
        for file in files:
            process_image(file, cursor)