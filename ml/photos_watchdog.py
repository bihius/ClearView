import logging
import os
from dotenv import load_dotenv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import photos
from db.db_utils import get_connection

load_dotenv()
logger = logging.getLogger(__name__)

images_path = os.getenv("IMAGES_PATH")


class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path == images_path:
            logger.info("New image detected: %s", event.src_path)
            photos.process_image(get_connection().cursor(), event.src_path)
            
def monitor_folder():
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, images_path, recursive=True)
    observer.start()
    
    try:
        logger.info("Monitoring folder: %s", images_path)
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        
