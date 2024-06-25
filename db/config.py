import os
from dotenv import load_dotenv

def get_dotenv_config():
    # Load configuration from .env file.
    load_dotenv("../.env")
    if os.getenv("POSTGRES_USER") and os.getenv("POSTGRES_HOST"):
        return {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT")
        }
    else:
        load_dotenv(".env")
        return {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT")
        }

