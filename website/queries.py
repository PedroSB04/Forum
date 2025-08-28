from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

from website.database import execute_sql

"""
# Query 2: Análise de Clientes e Fidelidade
def query_analise_clientes_fidelidade():
    # Análise de clientes por tempo de fidelidade e valor gerado
    # Subquery para calcular o tempo de fidelidade
    subquery_tempo_fidelidade = session.query(
        Cliente.id_cliente,
        Cliente.nome_cliente,
        Cliente.data_cadastro,
        func.current_date().label('data_atual'),
        func.extract('year', func.age(func.current_date(), Cliente.data_cadastro)).label('anos_fidelidade'),
        func.count(Venda.id_venda).label('total_compras'),
        func.sum(Venda.valor_total).label('valor_total_gasto')
    ).outerjoin(Venda, Cliente.id_cliente == Venda.id_cliente)\
     .group_by(Cliente.id_cliente, Cliente.nome_cliente, Cliente.data_cadastro)\
     .subquery()
    
    # Query principal com segmentação de clientes
    resultados = session.query(
        subquery_tempo_fidelidade.c.id_cliente,
        subquery_tempo_fidelidade.c.nome_cliente,
        subquery_tempo_fidelidade.c.data_cadastro,
        subquery_tempo_fidelidade.c.anos_fidelidade,
        subquery_tempo_fidelidade.c.total_compras,
        subquery_tempo_fidelidade.c.valor_total_gasto,
        case([
            (subquery_tempo_fidelidade.c.anos_fidelidade >= 5, "Cliente Ouro (5+ anos)"),
            (subquery_tempo_fidelidade.c.anos_fidelidade >= 3, "Cliente Prata (3-4 anos)"),
            (subquery_tempo_fidelidade.c.anos_fidelidade >= 1, "Cliente Bronze (1-2 anos)"),
        ], else_="Cliente Novo (<1 ano)").label('segmento_fidelidade'),
        case([
            (subquery_tempo_fidelidade.c.valor_total_gasto >= 10000, "VIP (R$10k+)"),
            (subquery_tempo_fidelidade.c.valor_total_gasto >= 5000, "Premium (R$5k-10k)"),
            (subquery_tempo_fidelidade.c.valor_total_gasto >= 1000, "Standard (R$1k-5k)"),
        ], else_="Basic (<R$1k)").label('segmento_valor'),
        func.avg(subquery_tempo_fidelidade.c.valor_total_gasto).over().label('media_geral_gasto'),
        func.percent_rank().over(order_by=subquery_tempo_fidelidade.c.valor_total_gasto).label('percentil_gasto')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_cliente': r.id_cliente,
        'nome_cliente': r.nome_cliente,
        'data_cadastro': r.data_cadastro,
        'anos_fidelidade': r.anos_fidelidade,
        'total_compras': r.total_compras,
        'valor_total_gasto': float(r.valor_total_gasto) if r.valor_total_gasto else 0,
        'segmento_fidelidade': r.segmento_fidelidade,
        'segmento_valor': r.segmento_valor,
        'media_geral_gasto': float(r.media_geral_gasto) if r.media_geral_gasto else 0,
        'percentil_gasto': float(r.percentil_gasto) if r.percentil_gasto else 0
    } for r in resultados])
    
    # Análises adicionais
    df['dias_ultima_compra'] = (datetime.now() - pd.to_datetime(df['data_cadastro'])).dt.days
    df['valor_medio_compra'] = df['valor_total_gasto'] / df['total_compras'].replace(0, 1)
    
    return df
"""

#implementar na barra de busca
def barra_de_busca(palavra):
    query = """
        SELECT
            username,
            conteudo,
            titulo
        FROM
            usuario
        JOIN
            post
        WHERE 
            username ILIKE %s OR
            conteudo ILIKE %s OR
            titulo ILIKE %s
    """
    params = (f"%{palavra}%", f"%{palavra}%", f"%{palavra}%")
    resultados = execute_sql(query, params, fetch=True)
    return resultados

#funções de interação com posts
def like(post_id):
    query = """
        UPDATE post
        SET likes = likes + 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def retirar_like(post_id):
    query = """
        UPDATE post
        SET likes = likes - 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def dislike(post_id):
    query = """
        UPDATE post
        SET dislikes = dislikes + 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def retirar_dislike(post_id):
    query = """
        UPDATE post
        SET dislikes = dislikes - 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def seguir(usuario_id):
    if usuario_id == current_user.id:
        raise ValueError("Você não pode seguir a si mesmo.")
    query = """
        INSERT INTO segue (seguidor_id, seguido_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    params = (current_user.id, usuario_id)
    execute_sql(query, params)

def deixar_seguir(usuario_id):
    if usuario_id == current_user.id:
        raise ValueError("Você não pode deixar de seguir a si mesmo.")
    query = """
        DELETE FROM segue
        WHERE seguidor_id = %s AND seguido_id = %s
    """
    params = (current_user.id, usuario_id)
    execute_sql(query, params)

#retorna as informações do perfil do usuário
def informacoes_perfil(usuario_id):
    query = """
        SELECT
            nome,
            username,
            email,
            foto_perfil,
            (SELECT COUNT(*) FROM segue WHERE seguido_id = %s) AS seguidores,
            (SELECT COUNT(*) FROM segue WHERE seguidor_id = %s) AS seguindo
        FROM
            usuario
        WHERE
            id = %s
    """
    params = (usuario_id, usuario_id, usuario_id)
    return execute_sql(query, params, fetch=True)

#funções de ordenação
def ordena_por_likes():
    query = "SELECT * FROM post ORDER BY likes DESC"
    return execute_sql(query, fetch=True)

def ordena_por_dislikes():
    query = "SELECT * FROM post ORDER BY dislikes DESC"
    return execute_sql(query, fetch=True)

def ordena_por_data_decrescente():
    query = "SELECT * FROM post ORDER BY data_post DESC"
    return execute_sql(query, fetch=True)

def ordena_por_data_crescente():
    query = "SELECT * FROM post ORDER BY data_post ASC"
    return execute_sql(query, fetch=True)

def filtrar_categoria(categoria):
    query = """
        SELECT * FROM post
        WHERE categoria = %s
    """
    params = (categoria,)
    return execute_sql(query, params, fetch=True)
