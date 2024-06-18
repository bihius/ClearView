import sys
from psycopg2 import connect, OperationalError, errors, errorcodes
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import get_dotenv_config
from init_db import init, init_schema_and_tables

def create_connection(config, dbname=None):
    # Create a connection to the PostgreSQL server.
    try:
        if dbname:
            config["dbname"] = dbname
        print(f"Connecting to the PostgreSQL server to database {dbname}")
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
            connection = connect(**get_dotenv_config())
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            init(connection)
            connection.close()
            return create_connection(config, dbname)
        if "password authentication failed" in str(e):
            print("Password authentication failed.")
            sys.exit(1)
        if "could not connect to server" in str(e):
            print("Could not connect to server.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Create connection unexpected error: {e}")
        sys.exit(1)

def self_test():
    # Perform a self-test to ensure the database and tables exist.
    try:
        print("Performing self-test...")
        connection = create_connection(get_dotenv_config(), dbname="clearview")
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM clearview.images LIMIT 1")
        print("Self-test successful")
        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"Operational error during self-test: {e}")
        sys.exit(1)
    except errors.lookup(errorcodes.UNDEFINED_TABLE):
        cursor = connection.cursor()
        init_schema_and_tables(cursor)
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Unexpected error during self-test: {e}")
        sys.exit(1)

def get_connection():
    # Get a connection to the 'clearview' database after performing a self-test.
    self_test()
    return create_connection(get_dotenv_config(), dbname="clearview")

if __name__ == "__main__":
    get_connection()
