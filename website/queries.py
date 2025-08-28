from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

from website.database import execute_sql

"""

"""

#implementar na barra de busca
def barra_de_busca(palavra, usuario_id):
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
    params = (f"%{palavra}%", f"%{palavra}%", f"%{palavra}%", f"%{palavra}%")
    resultados = execute_sql(query, params, fetch=True, usuario_id=usuario_id)
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
