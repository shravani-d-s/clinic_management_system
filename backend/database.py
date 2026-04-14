import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "system")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "XE")

def get_db_connection():
    try:
        # Construct DSN
        dsn_tns = oracledb.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
        # Create connection pool or direct connection
        # Since it's a small app, we can use a direct connection for simplicity
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=dsn_tns
        )
        # To automatically create dictionary mappings
        connection.autocommit = True
        return connection
    except oracledb.Error as error:
        print(f"Error connecting to Oracle Database: {error}")
        return None

def fetch_all_dict(cursor):
    """ Helper to fetch rows as dictionary """
    columns = [col[0].lower() for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    return cursor.fetchall()

def fetch_one_dict(cursor):
    """ Helper to fetch single row as dictionary """
    columns = [col[0].lower() for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    return cursor.fetchone()
