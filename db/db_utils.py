import sys
from psycopg2 import connect, OperationalError, errors, errorcodes
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config
from init_db import database_initialization, init_schema_and_tables
import logging


logger = logging.getLogger(__name__)

# Set up logging to file and console
# ! move it to main app file
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s - %(asctime)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('clearview.log'), 
        logging.StreamHandler(sys.stdout)
    ]
)

def create_connection(config, dbname=None):
    # Create a connection to the PostgreSQL server.
    try:
        if dbname:
            config["dbname"] = dbname
            logger.info("Creating connection to database: %s", dbname)
        else:
            logger.info("Creating connection to default database")
            
        connection = connect(
            dbname=config.get("dbname"),
            user=config.get("user"),
            password=config.get("password"),
            host=config.get("host"),
            port=config.get("port")
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    
    except OperationalError as e:
        if "does not exist" in str(e):
            connection = connect(**config.get_dotenv_config(), dbname="postgres")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            database_initialization(connection)
            connection.close()
            return create_connection(config, dbname)
        
        if "password authentication failed" in str(e):
            logger.error("Password authentication failed.")
            sys.exit(1)
            
        if "could not connect to server" in str(e):
            logger.error("Could not connect to server.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error creating connection: {e}")
        sys.exit(1)

def self_test():
    # Perform a self-test to ensure the database and tables exist.
    try:
        logger.info("Performing self-test")
        connection = create_connection(config.get_dotenv_config(), dbname="clearview")
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM clearview.images LIMIT 1")
        logger.info("Self-test passed")
        cursor.close()
        connection.close()
        
    except OperationalError as e:
        logger.error(f"Operational error during self-test: {e}")
        sys.exit(1)
        
    except errors.lookup(errorcodes.UNDEFINED_TABLE):

        init_schema_and_tables(connection.cursor())
        cursor.close()
        connection.close()
        
    except Exception as e:
        logger.error(f"Unexpected error during self-test: {e}")
        sys.exit(1)

def get_connection():
    # Get a connection to the 'clearview' database after performing a self-test.
    self_test()
    return create_connection(config.get_dotenv_config(), dbname="clearview")

if __name__ == "__main__":
    get_connection()
