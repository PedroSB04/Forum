import os
from flask import current_app, flash
from werkzeug.utils import secure_filename

import os
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from website.forms import FormpostPai, FormpostFilho
from website.database import execute_sql
from flask_login import current_user
from flask_login import login_required
from datetime import datetime
from werkzeug.utils import secure_filename



views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Recebe o filtro de ordenação e categoria da query string
    ordem = request.args.get('ordem', 'recentes')
    categoria_id = request.args.get('categoria', 'todas')
    if ordem == 'antigos':
        order_sql = 'ASC'
    else:
        order_sql = 'DESC'

    # Busca todas as categorias para o dropdown
    categorias = execute_sql("SELECT id_categoria, nome FROM categoria ORDER BY nome ASC", fetch=True)

    # Monta a query de posts com ou sem filtro de categoria
    if categoria_id and categoria_id != 'todas':
        query = f"""
            SELECT
                p.id_post,
                p.titulo,
                p.conteudo,
                p.data_post,
                p.likes,
                p.dislikes,
                u.username,
                u.foto_perfil,
                (SELECT COUNT(*) FROM post WHERE post_raiz_id = p.id_post) as total_respostas
            FROM post p
            JOIN usuario u ON p.id_usuario = u.id_usuario
            WHERE p.post_raiz_id IS NULL AND p.id_categoria = %s
            ORDER BY p.data_post {order_sql}
            LIMIT 20
        """
        posts = execute_sql(query, (categoria_id,), fetch=True)
    else:
        query = f"""
            SELECT
                p.id_post,
                p.titulo,
                p.conteudo,
                p.data_post,
                p.likes,
                p.dislikes,
                u.username,
                u.foto_perfil,
                (SELECT COUNT(*) FROM post WHERE post_raiz_id = p.id_post) as total_respostas
            FROM post p
            JOIN usuario u ON p.id_usuario = u.id_usuario
            WHERE p.post_raiz_id IS NULL
            ORDER BY p.data_post {order_sql}
            LIMIT 20
        """
        posts = execute_sql(query, fetch=True)

    # Formata a data dos posts para exibição mais amigável
    if posts:
        for post in posts:
            if post['data_post']:
                # Calcula tempo decorrido
                data_post = post['data_post']
                agora = datetime.now(data_post.tzinfo)
                diferenca = agora - data_post

                if diferenca.days > 0:
                    if diferenca.days == 1:
                        post['tempo_decorrido'] = '1 dia atrás'
                    else:
                        post['tempo_decorrido'] = f'{diferenca.days} dias atrás'
                elif diferenca.seconds >= 3600:
                    horas = diferenca.seconds // 3600
                    if horas == 1:
                        post['tempo_decorrido'] = '1 hora atrás'
                    else:
                        post['tempo_decorrido'] = f'{horas} horas atrás'
                elif diferenca.seconds >= 60:
                    minutos = diferenca.seconds // 60
                    if minutos == 1:
                        post['tempo_decorrido'] = '1 minuto atrás'
                    else:
                        post['tempo_decorrido'] = f'{minutos} minutos atrás'
                else:
                    post['tempo_decorrido'] = 'Agora mesmo'

    return render_template('index.html', posts=posts, ordem=ordem, categorias=categorias, categoria_id=categoria_id)

@views.route('/perfil/<int:id_usuario>')
@login_required
def perfil(id_usuario):
    # Busca as informações do usuário do perfil visitado
    usuario = execute_sql("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,), fetch_one=True)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('views.home'))

    qtd_posts_result = execute_sql("SELECT COUNT(*) FROM post WHERE id_usuario = %s AND post_raiz_id IS NULL", (id_usuario,), fetch_one=True)
    qtd_posts = qtd_posts_result['count'] if qtd_posts_result else 0

    # Busca quantidade de seguidores
    qtd_seguidores_result = execute_sql("SELECT COUNT(*) FROM segue WHERE seguido_id = %s", (id_usuario,), fetch_one=True)
    qtd_seguidores = qtd_seguidores_result['count'] if qtd_seguidores_result else 0

    # Busca quantidade de quem segue
    qtd_seguindo_result = execute_sql("SELECT COUNT(*) FROM segue WHERE seguidor_id = %s", (id_usuario,), fetch_one=True)
    qtd_seguindo = qtd_seguindo_result['count'] if qtd_seguindo_result else 0

    atividades = execute_sql("""
        SELECT
            p.id_post,
            p.titulo,
            p.conteudo,
            p.data_post,
            p.post_raiz_id,
            pai.titulo as titulo_pai
        FROM post p
        LEFT JOIN post pai ON p.post_raiz_id = pai.id_post
        WHERE p.id_usuario = %s
        ORDER BY p.data_post DESC
    """, (id_usuario,), fetch=True)

    pode_editar = current_user.is_authenticated and id_usuario == current_user.id_usuario

    # Cálculo dos dias como membro
    data_criacao = usuario['data_criacao']
    dias_membro = (datetime.now() - data_criacao).days if data_criacao else 0

    return render_template(
        'profile.html',
        usuario=usuario,
        qtd_posts=qtd_posts,
        dias_membro=dias_membro,
        qtd_seguidores=qtd_seguidores,
        qtd_seguindo=qtd_seguindo,
        atividades=atividades, # Passa a lista de atividades para o template
        pode_editar=pode_editar
    )


# Upload de avatar
@views.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    file = request.files.get('avatar')
    if not file or file.filename == '':
        flash('Nenhuma imagem selecionada.', 'warning')
        return redirect(url_for('views.perfil', id_usuario=current_user.id_usuario))

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        flash('Formato de imagem não suportado.', 'danger')
        return redirect(url_for('views.perfil', id_usuario=current_user.id_usuario))

    # Caminho para salvar o arquivo
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)
    new_filename = f'user_{current_user.id_usuario}{ext}'
    file_path = os.path.join(upload_folder, new_filename)
    file.save(file_path)

    # Caminho para acessar via web
    web_path = url_for('static', filename=f'uploads/avatars/{new_filename}')

    # Atualiza o campo foto_perfil no banco
    execute_sql("UPDATE usuario SET foto_perfil = %s WHERE id_usuario = %s", (web_path, current_user.id_usuario))

    flash('Foto de perfil atualizada com sucesso!', 'success')
    return redirect(url_for('views.perfil', id_usuario=current_user.id_usuario))

@views.route('/editar-perfil', methods=['POST'])
@login_required
def editar_perfil():
    # 1. Pega os dados enviados pelo formulário
    nome = request.form.get('nome')
    username = request.form.get('username')
    email = request.form.get('email')
    biografia = request.form.get('biografia')

    # 2. Atualiza os dados no banco de dados para o usuário logado
    execute_sql("""
        UPDATE usuario
        SET nome = %s, username = %s, email = %s, biografia = %s
        WHERE id_usuario = %s
    """, (nome, username, email, biografia, current_user.id_usuario))

    # 3. Exibe uma mensagem de sucesso
    flash('Perfil atualizado com sucesso!', 'success')

    # 4. Redireciona o usuário de volta para a página de perfil
    return redirect(url_for('views.perfil', id_usuario=current_user.id_usuario))

@views.route('/criarpost', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormpostPai()
    categorias = execute_sql("SELECT id_categoria, nome FROM categoria ORDER BY nome ASC", fetch=True)
    mensagem_categoria = None

    if form.validate_on_submit():
        id_categoria = request.form.get('categoria')
        if id_categoria:
            query = "INSERT INTO post (titulo, conteudo, id_usuario, id_categoria) VALUES (%s, %s, %s, %s)"
            params = (form.titulo.data, form.conteudo.data, current_user.id_usuario, id_categoria)
            execute_sql(query, params)
            return redirect(url_for('views.home'))
        else:
            mensagem_categoria = 'Selecione uma categoria.'
    return render_template('post.html', form=form, categorias=categorias, mensagem_categoria=mensagem_categoria)

@views.route('/discussao/<int:post_raiz_id>', methods=['GET', 'POST'])
def discussao(post_raiz_id):
    query_pai = """
        SELECT
            p.*,
            u.username,
            u.foto_perfil
        FROM post p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.id_post = %s
    """
    post_pai = execute_sql(query_pai, (post_raiz_id,), fetch_one=True)

    query_filhos = """
        SELECT
            p.*,
            u.username,
            u.foto_perfil
        FROM post p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.post_raiz_id = %s
        ORDER BY p.data_post ASC
    """
    posts_filhos = execute_sql(query_filhos, (post_raiz_id,), fetch=True)

    form = FormpostFilho()
    form.post_raiz_id.data = post_raiz_id

    if form.validate_on_submit():
        query = "INSERT INTO post (titulo, conteudo, id_usuario, post_raiz_id) VALUES (%s, %s, %s, %s)"
        params = (None, form.conteudo.data, current_user.id_usuario, post_raiz_id)
        execute_sql(query, params)
        return redirect(url_for('views.discussao', post_raiz_id=post_raiz_id))

    return render_template(
        'discussao.html',
        post_pai=post_pai,
        posts_filhos=posts_filhos,
        form=form
    )

# NOVO: Rota para deletar um post/comentário
@views.route('/deletar-post/<int:id_post>', methods=['POST'])
@login_required
def deletar_post(id_post):
    # 1. Verifica se o post existe e pertence ao usuário logado
    post = execute_sql("SELECT id_post, id_usuario FROM post WHERE id_post = %s", (id_post,), fetch_one=True)

    if post and post['id_usuario'] == current_user.id_usuario:
        # 2. Se sim, deleta o post
        execute_sql("DELETE FROM post WHERE id_post = %s", (id_post,))
        flash('Publicação removida com sucesso.', 'success')
    else:
        # 3. Se não, exibe um erro
        flash('Você não tem permissão para remover esta publicação.', 'danger')

    # 4. Redireciona de volta para a página de perfil do usuário
    return redirect(url_for('views.perfil', id_usuario=current_user.id_usuario))