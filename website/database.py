import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': 'localhost',
    'database': 'dev_forum_container',
    'user': 'postgres',
    'password': 'pedro951',
    'port': '5433'
}

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados usando o DB_CONFIG.
    """
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# 1. Abre uma conexão com o banco usando as configurações do DB_CONFIG.
# 2. Executa a query SQL recebida como argumento, com ou sem parâmetros (params).
# 3. Se você passar:
# fetch_one=True: retorna apenas uma linha do resultado (um dicionário).
# fetch=True: retorna todas as linhas do resultado (lista de dicionários).
# Se nenhum dos dois: executa a query (útil para INSERT, UPDATE, DELETE), faz o commit e retorna o número de linhas afetadas.
# 4. Se ocorrer erro, faz rollback e imprime o erro.
# 5. Fecha o cursor e a conexão ao final.
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

# Teste rápido de conexão
if __name__ == "__main__":
    try:
        resultado = execute_sql("SELECT 1", fetch_one=True)
        print("Conexão bem-sucedida! Resultado:", resultado)
    except Exception as e:
        print("Falha na conexão com o banco de dados:", e)