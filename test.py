import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "ml")))

def main():
    connection = importlib.import_module("db.db_utils").get_connection()
    
main()
    