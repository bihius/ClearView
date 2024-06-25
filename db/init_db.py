import sys
from config import get_dotenv_config
from psycopg2 import OperationalError, errors, errorcodes
import logging

logger = logging.getLogger(__name__)

def database_initialization(connection):
    create_database(connection.cursor())
    create_schema(connection.cursor())
    for query in create_table_queries:
        if type(query) == dict:
            for table_name, table_query in query.items():
                create_table(connection.cursor(), table_name, table_query)
        else:
            connection.cursor().execute(query)
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

def create_schema(cursor):
    logger.info("Creating schema 'clearview'")
    
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS clearview")
        
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        sys.exit(1)
    except OperationalError as e:
        logger.error(f"Operational error creating schema: {e}")
        sys.exit(1)
        
    logger.info("Schema 'clearview' created successfully")
    
def create_table(cursor, table_name, table_query):
    logger.info(f"Creating table '{table_name}'")
    
    try:
        cursor.execute(table_query)
        
    except Exception as e:
        logger.error(f"Error creating table '{table_name}': {e}")
        sys.exit(1)
        
    except OperationalError as e:
        logger.error(f"Operational error creating table '{table_name}': {e}")
        sys.exit(1)
        
    logger.info(f"Table '{table_name}' created successfully")
    
create_table_queries = [{"images": "CREATE TABLE IF NOT EXISTS clearview.images (id SERIAL PRIMARY KEY, name TEXT, path TEXT, hash TEXT, vector BYTEA)"}, {"paths": "CREATE TABLE IF NOT EXISTS clearview.paths (id SERIAL PRIMARY KEY, path TEXT)"}, "CREATE TABLE IF NOT EXISTS clearview.paths (id SERIAL PRIMARY KEY, path TEXT)"]