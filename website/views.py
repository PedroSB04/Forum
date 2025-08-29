from flask import Blueprint, render_template, redirect, url_for
from website.forms import FormpostPai, FormpostFilho
from website.database import execute_sql
from flask_login import current_user
from flask_login import login_required
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/perfil/<int:id_usuario>')
@login_required
def perfil(id_usuario):
    # Busca as informações do usuário do perfil visitado
    usuario = execute_sql("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,), fetch_one=True)

    # Busca quantidade de posts
    qtd_posts = execute_sql("SELECT COUNT(*) FROM post WHERE id_usuario = %s", (id_usuario,), fetch_one=True)
    qtd_posts = qtd_posts['count'] if qtd_posts else 0

    # Busca quantidade de seguidores
    qtd_seguidores = execute_sql("SELECT COUNT(*) FROM segue WHERE seguido_id = %s", (id_usuario,), fetch_one=True)
    qtd_seguidores = qtd_seguidores['count'] if qtd_seguidores else 0

    # Busca quantidade de quem segue
    qtd_seguindo = execute_sql("SELECT COUNT(*) FROM segue WHERE seguidor_id = %s", (id_usuario,), fetch_one=True)
    qtd_seguindo = qtd_seguindo['count'] if qtd_seguindo else 0

    # Busca listas (opcional)
    seguidores = execute_sql("""
        SELECT u.id_usuario, u.nome, u.username FROM usuario u
        JOIN segue s ON u.id_usuario = s.seguidor_id
        WHERE s.seguido_id = %s
    """, (id_usuario,), fetch=True)

    seguindo = execute_sql("""
        SELECT u.id_usuario, u.nome, u.username FROM usuario u
        JOIN segue s ON u.id_usuario = s.seguido_id
        WHERE s.seguidor_id = %s
    """, (id_usuario,), fetch=True)

    if current_user.is_authenticated and int(id_usuario) == current_user.id_usuario:
        # Usuário está vendo o próprio perfil
        usuario = execute_sql("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,), fetch_one=True)
        pode_editar = True
    else:
        usuario = execute_sql("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,), fetch_one=True)
        pode_editar = False

    # Cálculo dos dias como membro
    data_criacao = usuario['data_criacao']  # Supondo que já é um objeto datetime
    if isinstance(data_criacao, str):
        data_criacao = datetime.strptime(data_criacao, '%Y-%m-%d')  # ajuste o formato se necessário

    dias_membro = (datetime.now() - data_criacao).days if data_criacao else ''

    return render_template(
        'profile.html',
        usuario=usuario,
        qtd_posts=qtd_posts,
        dias_membro=dias_membro,
        qtd_seguidores=qtd_seguidores,
        qtd_seguindo=qtd_seguindo,
        seguidores=seguidores,
        seguindo=seguindo,
        pode_editar=pode_editar
    )

@views.route('/criarpost', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormpostPai()
    if form.validate_on_submit():
        query = "INSERT INTO post (titulo, conteudo, id_usuario) VALUES (%s, %s, %s)"
        params = (form.titulo.data, form.conteudo.data, current_user.id_usuario)
        execute_sql(query, params)
    return render_template('post.html', form=form)

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