import sys
from config import get_dotenv_config
from psycopg2 import OperationalError, errors, errorcodes
import logging

logger = logging.getLogger(__name__)


def database_initialization(connection):
    create_database(connection.cursor())
    init_schema_and_tables(connection.cursor())
    connection.cursor().close()
    connection.close()

def create_database(cursor):
    # Create the database 'clearview' if it doesn't exist.
    logging.INFO("Creating database 'clearview'")
    cursor.execute("SELECT datname FROM pg_database WHERE datname='clearview'")
    
    if ("clearview",) not in cursor.fetchall():
        cursor.execute("CREATE DATABASE clearview")
    else:
        logging.warning("Database 'clearview' already exists")
        choice = input("Do you want to drop the database? (y/n): ")
        
        if choice.lower() == "y":
            logging.warning("Dropping database 'clearview'")
            cursor.execute("DROP DATABASE clearview")
            cursor.execute("CREATE DATABASE clearview")
            
        else:
            logging.warning("Exiting with no changes made.")
            sys.exit()
            
    logging.INFO("Database 'clearview' created successfully")
    cursor.close()

def init_schema_and_tables(cursor):
    logging.INFO("Creating schema and tables")
    
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS clearview")
        
    except Exception as e:
        logging.error(f"Error creating schema: {e}")
        sys.exit(1)
    except OperationalError as e:
        logging.error(f"Operational error creating schema: {e}")
        sys.exit(1)
    logging.INFO("Schema 'clearview' created successfully")
    
    try:
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS clearview.images (
        id SERIAL PRIMARY KEY,
        name TEXT,
        url TEXT,
        vector BYTEA
    )
    """)
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        sys.exit(1)
    except OperationalError as e:
        logging.error(f"Operational error creating table: {e}")
        sys.exit(1)
    
    logging.INFO("Table 'images' created successfully")
    

if __name__ == "__main__":
    database_initialization()
