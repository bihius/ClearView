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
    logger.info("Creating database 'clearview'")
    cursor.execute("SELECT datname FROM pg_database WHERE datname='clearview'")
    
    if ("clearview",) not in cursor.fetchall():
        cursor.execute("CREATE DATABASE clearview")
    else:
        logger.warning("Database 'clearview' already exists")
        choice = input("Do you want to drop the database? (y/n): ")
        
        if choice.lower() == "y":
            logger.warning("Dropping database 'clearview'")
            cursor.execute("DROP DATABASE clearview")
            cursor.execute("CREATE DATABASE clearview")
            
        else:
            logger.warning("Exiting with no changes made.")
            sys.exit()
            
    logger.info("Database 'clearview' created successfully")
    cursor.close()

def init_schema_and_tables(cursor):
    logger.info("Creating schema and tables")
    
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS clearview")
        
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        sys.exit(1)
    except OperationalError as e:
        logger.error(f"Operational error creating schema: {e}")
        sys.exit(1)
        
    logger.info("Schema 'clearview' created successfully")
    
    try:
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS clearview.images (
        id SERIAL PRIMARY KEY,
        name TEXT,
        path TEXT,
        hash TEXT,
        vector BYTEA
    )
    """)
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        sys.exit(1)
    except OperationalError as e:
        logger.error(f"Operational error creating table: {e}")
        sys.exit(1)
    
    logger.info("Table 'images' created successfully")
