import psycopg2

try:
    # Configuração da conexão
    conn = psycopg2.connect(
        host="localhost",
        database="dev_forum",
        user="postgres",
        password="12345"
    )
    
    cursor = conn.cursor()
    
    # Teste rápido: pegar versão do PostgreSQL
    cursor.execute("SELECT version();")
    resultado = cursor.fetchone()
    print("Conexão bem-sucedida!")
    print("Versão do banco:", resultado[0])
    
    cursor.close()
    conn.close()

except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)