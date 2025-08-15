from flask import Blueprint, render_template, redirect, url_for
from website.forms import FormpostPai, FormpostFilho
from website.database import execute_sql
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/perfil')
def perfil():
    return render_template('perfil.html')

@views.route('/criarpost', methods=['GET', 'POST'])
def criar_post():
    form = FormpostPai()
    if form.validate_on_submit():
        query = "INSERT INTO post (titulo, conteudo, id_usuario) VALUES (%s, %s, %s)"
        params = (form.titulo.data, form.conteudo.data, current_user.id_usuario)
        execute_sql(query, params)
    return render_template('posts.html', form=form)

@views.route('/discussao/<int:post_raiz_id>', methods=['GET', 'POST'])
def discussao(post_raiz_id):
    # Busca o post pai
    query_pai = "SELECT * FROM post WHERE id_post = %s"
    post_pai = execute_sql(query_pai, (post_raiz_id,), fetch_one=True)

    # Busca todos os posts filhos ligados a esse pai
    query_filhos = "SELECT * FROM post WHERE post_raiz_id = %s"
    posts_filhos = execute_sql(query_filhos, (post_raiz_id,), fetch=True)

    # Formulário para novo post filho
    form = FormpostFilho()
    form.post_raiz_id.data = post_raiz_id  # Preenche o campo oculto

    if form.validate_on_submit():
        query = "INSERT INTO post (conteudo, id_usuario, post_raiz_id) VALUES (%s, %s, %s)"
        params = (form.conteudo.data, current_user.id_usuario, post_raiz_id)
        execute_sql(query, params)
        return redirect(url_for('views.discussao', post_raiz_id=post_raiz_id))

    return render_template(
        'discussao.html',
        post_pai=post_pai,
        posts_filhos=posts_filhos,
        form=form
    )

