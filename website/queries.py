from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

from website.database import execute_sql

"""
# Query 1: Análise de Vendas por Categoria e Período
def query_vendas_por_categoria_periodo():
    # Configuração da sessão
    session = db.Session()

    # Subquery para vendas por categoria
    subquery_vendas = session.query(
        Categoria.nome_categoria,
        func.date_trunc('month', Venda.data_venda).label('mes'),
        func.sum(Venda.valor_total).label('total_vendas'),
        func.count(Venda.id_venda).label('quantidade_vendas'),
        func.avg(Venda.valor_total).label('valor_medio_venda'),
        func.sum(Venda.quantidade).label('total_itens_vendidos'),
        func.max(Venda.valor_total).label('maior_venda'),
        func.min(Venda.valor_total).label('menor_venda')
    ).join(Produto, Venda.id_produto == Produto.id_produto)\
     .join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .filter(Venda.data_venda.between('2023-01-01', '2023-12-31'))\
     .group_by(Categoria.nome_categoria, func.date_trunc('month', Venda.data_venda))\
     .subquery()
    
    # Query principal com cálculos adicionais
    resultados = session.query(
        subquery_vendas.c.nome_categoria,
        subquery_vendas.c.mes,
        subquery_vendas.c.total_vendas,
        subquery_vendas.c.quantidade_vendas,
        subquery_vendas.c.valor_medio_venda,
        subquery_vendas.c.total_itens_vendidos,
        subquery_vendas.c.maior_venda,
        subquery_vendas.c.menor_venda,
        func.percentile_cont(0.5).within_group(
            subquery_vendas.c.total_vendas
        ).label('mediana_vendas'),
        func.stddev(subquery_vendas.c.total_vendas).label('desvio_padrao_vendas'),
        func.var_samp(subquery_vendas.c.total_vendas).label('variancia_vendas'),
        func.rank().over(
            partition_by=subquery_vendas.c.mes,
            order_by=subquery_vendas.c.total_vendas.desc()
        ).label('ranking_vendas'),
        func.rank().over(
            partition_by=subquery_vendas.c.mes,
            order_by=subquery_vendas.c.quantidade_vendas.desc()
        ).label('ranking_quantidade')
    ).all()
    
    # Processamento adicional dos resultados
    df = pd.DataFrame([{
        'categoria': r.nome_categoria,
        'mes': r.mes,
        'total_vendas': float(r.total_vendas) if r.total_vendas else 0,
        'quantidade_vendas': r.quantidade_vendas,
        'valor_medio_venda': float(r.valor_medio_venda) if r.valor_medio_venda else 0,
        'total_itens': r.total_itens_vendidos,
        'maior_venda': float(r.maior_venda) if r.maior_venda else 0,
        'menor_venda': float(r.menor_venda) if r.menor_venda else 0,
        'mediana': float(r.mediana_vendas) if r.mediana_vendas else 0,
        'desvio_padrao': float(r.desvio_padrao_vendas) if r.desvio_padrao_vendas else 0,
        'variancia': float(r.variancia_vendas) if r.variancia_vendas else 0,
        'ranking_vendas': r.ranking_vendas,
        'ranking_quantidade': r.ranking_quantidade
    } for r in resultados])
    
    # Cálculos adicionais com pandas
    df['percentual_crescimento'] = df.groupby('categoria')['total_vendas'].pct_change() * 100
    df['media_movel'] = df.groupby('categoria')['total_vendas'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    
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
