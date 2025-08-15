from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

novo_usuario = db.User (
    Formsignup.username.data,
    Formsignup.email.data,
    Formsignup.senha.data
)
db.session.add(novo_usuario)
db.session.commit()

novo_post = db.Post(
    titulo = request.form['titulo'],
    conteudo = request.form['conteudo'],
    username = current_user.username
)
db.session.add(novo_post)
db.session.commit()

novo_comentario = db.Comentario(
    conteudo = request.form['conteudo'],
    post_id = novo_post.id,
    username = current_user.username
)
db.session.add(novo_comentario)
db.session.commit()

def Like(post_id):
    post = db.Post.query.get(post_id)
    post.likes += 1
    db.session.commit()

def Tirar_Like(post_id):
    post = db.Post.query.get(post_id)
    post.likes -= 1
    db.session.commit()

def Dislike(post_id):
    post = db.Post.query.get(post_id)
    post.dislikes += 1
    db.session.commit()

def Tirar_Dislike(post_id):
    post = db.Post.query.get(post_id)
    post.dislikes -= 1
    db.session.commit()

def Seguir(usuario_id):
    if usuario_id == current_user.id:
        raise ValueError("Você não pode seguir a si mesmo.")
    usuario = db.User.query.get(usuario_id)
    usuario.seguindo += 1
    db.session.commit()

def Deixar_Seguir(usuario_id):
    usuario = db.User.query.get(usuario_id)
    usuario.seguindo -= 1
    db.session.commit()

def Buscar_Posts_Por_Usuario(usuario_id):
    return db.Post.query.filter_by(usuario_id=usuario_id).all()

def Buscar_Comentarios_Por_Post(post_id):
    return db.Comentario.query.filter_by(post_id=post_id).all()

def Buscar_Posts_Por_Likes():
    return db.Post.query.order_by(db.Post.likes.desc()).all()

def Buscar_Posts_Por_Dislikes():
    return db.Post.query.order_by(db.Post.dislikes.desc()).all()

def Informacoes_Perfil(usuario_id):
    usuario = db.User.query.get(usuario_id)
    if not usuario:
        return None
    return {
        "nome de usuário": usuario.username,
        "seguindo": usuario.seguindo,
        "seguidores": usuario.seguidores,
        "posts": Buscar_Posts_Por_Usuario(usuario_id)
    }

