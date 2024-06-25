import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "ml")))

def main():
    connection = importlib.import_module("db.db_utils").get_connection()
    connection.cursor().execute("SELECT * FROM clearview.images")
    
    # image_path = "./images/test1.jpg"

    # importlib.import_module("ml.photos").process_image(connection.cursor(), image_path)
        
main()
    