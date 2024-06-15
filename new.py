import os
import requests
from dotenv import load_dotenv
import json
import psycopg2
from psycopg2 import sql

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

SUPABASE_URL = "http://10.15.10.254:8000"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q"
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
POSTGRES_DB = os.getenv('DB_NAME')
POSTGRES_HOST = os.getenv('DB_HOST')
POSTGRES_PORT = os.getenv('DB_PORT')


def generate_service_role_key():
    url = f"{SUPABASE_URL}/auth/v1/admin/users"
    headers = {
        "apiKey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": "k.kasperkiewicz@proton.me",
        "password": "test12345",
        "role": "service_role",
        # "email_confirm": "True"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error generating service role key: {response.status_code}, {response.text}")
        return None


def grant_permissions():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()
        permissions_query = """
        GRANT USAGE ON SCHEMA auth TO postgres;
        GRANT SELECT, UPDATE ON ALL TABLES IN SCHEMA auth TO postgres;
        """
        cursor.execute(permissions_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Permissions granted successfully.")
    except Exception as e:
        print(f"Error granting permissions: {e}")


def confirm_user_email_in_db(user_id):
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()
        query = sql.SQL("UPDATE auth.users SET email_confirmed_at = now() WHERE id = %s")
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Email confirmed in database successfully.")
    except psycopg2.errors.InsufficientPrivilege as e:
        print(f"Error confirming email in database: {e}")
        print("Attempting to grant permissions...")
        grant_permissions()
        # Retry the operation after granting permissions
        try:
            conn = psycopg2.connect(
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )
            cursor = conn.cursor()
            query = sql.SQL("UPDATE auth.users SET email_confirmed_at = now() WHERE id = %s")
            cursor.execute(query, (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print("Email confirmed in database successfully on retry.")
        except Exception as e:
            print(f"Retry failed: {e}")
    except Exception as e:
        print(f"Error confirming email in database: {e}")


def login_user(email, password):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_API_KEY,
    }
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error logging in: {response.status_code}, {response.text}")
        return None


def main():
    user_data = generate_service_role_key()
    if user_data:
        user_id = user_data['id']
        confirm_user_email_in_db(user_id)

        login_response = login_user(user_data['email'], "test12345")
        if login_response:
            new_token = login_response['access_token']
            print(f"Generated new token: {new_token}")
            # Możesz teraz użyć tego tokenu do dalszych operacji
            headers = {
                "apiKey": new_token,
                "Authorization": f"Bearer {new_token}"
            }
            # Przykładowe zapytanie do Supabase
            response = requests.get(f"{SUPABASE_URL}/rest/v1/your-table", headers=headers)
            print(response.json())
        else:
            print("Failed to log in and get a new token.")
    else:
        print("Failed to generate a new user.")


if __name__ == "__main__":
    main()
