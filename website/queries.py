from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

from website.database import execute_sql

# novo_usuario = db.User (
#     Formsignup.username.data,
#     Formsignup.email.data,
#     Formsignup.senha.data
# )
# db.session.add(novo_usuario)
# db.session.commit()

# novo_post = db.Post(
#     titulo = request.form['titulo'],
#     conteudo = request.form['conteudo'],
#     username = current_user.username
# )
# db.session.add(novo_post)
# db.session.commit()

# novo_comentario = db.Comentario(
#     conteudo = request.form['conteudo'],
#     post_id = novo_post.id,
#     username = current_user.username
# )
# db.session.add(novo_comentario)
# db.session.commit()

# def Like(post_id):
#     post = db.Post.query.get(post_id)
#     post.likes += 1
#     db.session.commit()

# def Tirar_Like(post_id):
#     post = db.Post.query.get(post_id)
#     post.likes -= 1
#     db.session.commit()

# def Dislike(post_id):
#     post = db.Post.query.get(post_id)
#     post.dislikes += 1
#     db.session.commit()

# def Tirar_Dislike(post_id):
#     post = db.Post.query.get(post_id)
#     post.dislikes -= 1
#     db.session.commit()

# def Seguir(usuario_id):
#     if usuario_id == current_user.id:
#         raise ValueError("Você não pode seguir a si mesmo.")
#     usuario = db.User.query.get(usuario_id)
#     usuario.seguindo += 1
#     db.session.commit()

# def Deixar_Seguir(usuario_id):
#     usuario = db.User.query.get(usuario_id)
#     usuario.seguindo -= 1
#     db.session.commit()

# def Buscar_Posts_Por_Usuario(usuario_id):
#     return db.Post.query.filter_by(usuario_id=usuario_id).all()

# def Buscar_Comentarios_Por_Post(post_id):
#     return db.Comentario.query.filter_by(post_id=post_id).all()

# def Buscar_Posts_Por_Likes():
#     return db.Post.query.order_by(db.Post.likes.desc()).all()

# def Buscar_Posts_Por_Dislikes():
#     return db.Post.query.order_by(db.Post.dislikes.desc()).all()

# def Informacoes_Perfil(usuario_id):
#     usuario = db.User.query.get(usuario_id)
#     if not usuario:
#         return None
#     return {
#         "nome de usuário": usuario.username,
#         "seguindo": usuario.seguindo,
#         "seguidores": usuario.seguidores,
#         "posts": Buscar_Posts_Por_Usuario(usuario_id)
#     }
###########################

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
