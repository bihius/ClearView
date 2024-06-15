import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
from strings import createDatabaseQuery, testConnectionQuery

subdir = Path(__file__).parent.parent
dotenv_path = subdir / '.env'

load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set")

def createConnection() -> Client:
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set")

        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def testConnection():
    client = createConnection()
    if client:
        try:

            print("Connection successful")
            print(response)
        except Exception as e:
            print("Error: " + str(e))


def checkIfDatabaseExists():
    client = createConnection()
    if client:
        try:
            response = client.table("images").select("*").limit(1).execute()
            if not response.data:
                print("Table does not exist")
                return False
            return True
        except Exception as e:
            if '42P01' in str(e):
                print("Table does not exist (42P01)")
                return False
            print(f"Error checking table existence: {e}")
            return False

def createDatabase():
    client = createConnection()
    if client:
        try:
            response = client.rpc("execute_sql", {"sql": createDatabaseQuery})
            print(response.data)
        except Exception as e:
            print(f"Error initializing table: {e}")

testConnection()
#if not checkIfDatabaseExists():
#    createDatabase()

