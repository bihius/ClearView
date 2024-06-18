import sys
from config import get_dotenv_config
from psycopg2 import OperationalError, errors, errorcodes


def init(connection):
    # Initialize the database and schema.
    try: 
        create_database(connection.cursor())
    except OperationalError as e:
        print(f"Operational error during initialization: {e}")
        sys.exit(1)
    except errors.lookup(errorcodes.DUPLICATE_DATABASE):
        print("Database already exists.")
    except Exception as e:
        print(f"Unexpected error during initialization: {e}")
        sys.exit(1)

def create_database(cursor):
    # Create the database 'clearview' if it doesn't exist.
    print("Creating database...")
    cursor.execute("SELECT datname FROM pg_database WHERE datname='clearview'")
    if ("clearview",) not in cursor.fetchall():
        cursor.execute("CREATE DATABASE clearview")
    else:
        print("Database already exists")
        choice = input("Do you want to drop the database? (y/n): ")
        if choice.lower() == "y":
            cursor.execute("DROP DATABASE clearview")
            cursor.execute("CREATE DATABASE clearview")
        else:
            print("Exiting")
            sys.exit()
    print("Database created successfully")
    cursor.close()

def init_schema_and_tables(cursor):
    print("Table 'images' does not exist. Creating table.")
    # Create the 'clearview' schema and the 'images' table if they don't exist.
    cursor.execute("CREATE SCHEMA IF NOT EXISTS clearview")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clearview.images (
        id SERIAL PRIMARY KEY,
        name TEXT,
        url TEXT,
        vector BYTEA
    )
    """)
    print("Table 'images' created successfully.")

if __name__ == "__main__":
    init()
