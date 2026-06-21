import psycopg2 
from db_secrets import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )