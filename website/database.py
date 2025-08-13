import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="dev_forum",
        user="postgres",
        password="12345"
    )
    return conn

