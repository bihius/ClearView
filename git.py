from db.db_utils import create_connection
import ml.init

from dotenv import load_dotenv

load_dotenv()

def main():
    create_connection()
    
main()
    