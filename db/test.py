import os
import random
import string
import psycopg2
from psycopg2 import sql
from supabase import create_client, Client
from dotenv import load_dotenv, set_key
import requests

# Funkcja do generowania losowych haseł
def generate_random_password(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


# Funkcja do sprawdzania istnienia pliku .env i wczytywania zmiennych środowiskowych
def load_env():
    if os.path.exists("../.env"):
        load_dotenv()
        return True
    else:
        print("Plik .env nie istnieje.")
        return False


# Funkcja do tworzenia połączenia z bazą danych PostgreSQL
def create_connection(dbname, user, password, host, port):
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )


def close_connection(conn, cur):
    cur.close()
    conn.close()

# Funkcja do sprawdzania i aktualizacji użytkownika PostgreSQL
def check_and_create_user():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if db_user == "postgres":
        new_user = generate_random_password()
        new_password = generate_random_password()

        conn = create_connection("postgres", db_user, db_password, db_host, db_port)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(new_user)), [new_password])
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(sql.Identifier(db_name), sql.Identifier(new_user)))

        cur.execute(sql.SQL("GRANT USAGE ON SCHEMA clearview TO {}").format(sql.Identifier(new_user)))
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA clearview TO {}").format(sql.Identifier(new_user)))
        cur.close()
        conn.close()
        set_key('../.env', 'DB_USER', new_user)
        set_key('../.env', 'DB_PASSWORD', new_password)
        print(f"Utworzono nowego użytkownika: {new_user} z hasłem: {new_password}")



# Funkcja do sprawdzania i aktualizacji bazy danych PostgreSQL
def check_and_create_database():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    new_db_name = "clearview_db"

    conn = psycopg2.connect(
        dbname='postgres',  # Łączymy się z domyślną bazą danych
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Sprawdzenie, czy nowa baza danych już istnieje
    cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [new_db_name])
    exists = cur.fetchone()
    if exists:
        print(f"Baza danych '{new_db_name}' już istnieje.")
    else:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
        print(f"Utworzono nową bazę danych: {new_db_name}")
        set_key('.env', 'DB_NAME', new_db_name)

    cur.close()
    conn.close()




# Funkcja do tworzenia schematu i tabeli w PostgreSQL
def create_schema_and_table():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    conn = create_connection(db_name, db_user, db_password, db_host, db_port)
    cur = conn.cursor()

    schema_name = "clearview"
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
    if cur.fetchone() is None:
        create_schema_query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name))
        cur.execute(create_schema_query)
        conn.commit()
        print(f"Schema '{schema_name}' created successfully.")
    else:
        print(f"Schema '{schema_name}' already exists.")

    table_name = "images"
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name = %s",
                (schema_name, table_name))
    if cur.fetchone() is None:
        create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}.{} (
            id SERIAL PRIMARY KEY,
            image_url TEXT NOT NULL,
            image_name TEXT NOT NULL,
            image_hash TEXT NOT NULL,
            image_features FLOAT8[]
        )
        """).format(sql.Identifier(schema_name), sql.Identifier(table_name))
        cur.execute(create_table_query)
        conn.commit()
        print(f"Table '{schema_name}.{table_name}' created successfully.")
    else:
        print(f"Table '{schema_name}.{table_name}' already exists.")

    close_connection(conn, cur)


# Funkcja do dodawania dokumentów przez Supabase
def add_document_via_supabase(image_url: str, image_name: str, image_hash: str, image_features: list):
    schema_name = "clearview"
    table_name = "images"
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    supabase: Client = create_client(supabase_url, supabase_key)
    print(
        f"Adding image '{image_name}, image hash: {image_hash}, image features: {image_features}, image_url: {image_url}")
    try:
        data = {
            "image_url": image_url,
            "image_name": image_name,
            "image_hash": image_hash,
            "image_features": image_features
        }
        response = supabase.table("images").insert(data, returning="minimal").execute()
        print(f"Document added successfully: {response}")
    except Exception as e:
        print(f"Failed to add document via Supabase: {e}")


def generate_new_supabase_key():
    headers = {
        'Content-Type': 'application/json',
        'apikey': os.getenv("SUPABASE_KEY"),
        'Authorization': f'Bearer {os.getenv("SUPABASE_TOKEN")}',
    }

    payload = {
        "name": "Buahahaha",
        "role": "anon",
        "expiry_date": None
    }

    response = requests.post(f'{os.getenv("SUPABASE_URL")}/rest/v1/auth/keys', headers=headers, json=payload)

    if response.status_code == 201:
        new_key = response.json()['api_key']
        set_key('../.env', 'SUPABASE_KEY', new_key)
        print(f"Utworzono nowy klucz API Supabase: {new_key}")
        return new_key
    else:
        print(f"Failed to create new Supabase API key: {response.status_code}, {response.text}")
        return None

# Główne wywołanie skryptu
if load_env():
    # generate_new_supabase_key()
    # check_and_create_user()
    # check_and_create_database()
    # check_and_update_supabase_key()
    # create_schema_and_table()

    # Przykład dodania nowego dokumentu
    image_url = "https://example.com/image"
    image_name = "test_image"
    image_hash = "c62261691dade15bb445fc67e7d6eb97"
    image_features = [0.1, 0.2, 0.3]

    SUPABASE_URL = "http://10.15.10.254:8000"
    SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q"

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
    response = supabase.auth.admin({
        "email": "test@local.com",
        "password": "test12345",
        "email_confirmed": True,
    })


    # add_document_via_supabase(image_url, image_name, image_hash, image_features)

