import logging
import hashlib

logger = logging.getLogger(__name__)

# hello there, general kenobi

def calculate_md5(image_path):
    with open(image_path, 'rb') as f:
        try:
            data = f.read()
            return hashlib.md5(data).hexdigest()
        except Exception as e:
            logger.error(f"Error while calculating md5 for {image_path}: {e}")
            return False
        
def check_image_exist(cursor, image_hash):
    # don't know if that have sense
    cursor.execute("SELECT * FROM clearview.images WHERE hash = %s", (image_hash,))
    if cursor.fetchone():
        return True
    else:
        return False

def image_to_db(cursor, image_path, image_hash):
    cursor.execute("""
        INSERT INTO clearview.images (name, path, hash)
        VALUES (%s, %s, %s)
    """, (image_path.split("/")[-1], image_path, image_hash))
    
def process_image(cursor, image_path):
    image_hash = calculate_md5(image_path)
    if not check_image_exist(cursor, image_hash):
        image_to_db(cursor, image_path, image_hash)
        logger.info(f"Image {image_path} added to database")
    else:
        logger.info(f"Image {image_path} already exists in database")
        
