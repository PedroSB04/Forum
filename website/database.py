import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': 'localhost',
    'database': 'dev_forum',
    'user': 'postgres',
    'password': '12345',
    'port': '5432'
}

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados usando o DB_CONFIG.
    """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def execute_sql(query, params=None, fetch=False, fetch_one=False):
    """
    Executa uma query SQL.
    - fetch=True retorna todas as linhas.
    - fetch_one=True retorna apenas uma linha.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if fetch_one:
            return cursor.fetchone()
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print("Erro SQL:", e)
    finally:
        cursor.close()
        conn.close()