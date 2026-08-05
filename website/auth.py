from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from website.database import execute_sql
from website.forms import Formlogin, Formsignup
from website.models import Usuario

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Formlogin()
    erro = None
    if form.validate_on_submit():
        print("Formulário validado!")
        print("Email:", form.email.data)
        print("Senha:", form.senha.data)
        query = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        params = (form.email.data, form.senha.data)
        usuario = execute_sql(query, params, fetch_one=True)
        print("Usuário encontrado:", usuario)
        if usuario:
            usuario_obj = Usuario(**usuario)
            login_user(usuario_obj)
            return redirect(url_for('views.perfil', id_usuario=usuario['id_usuario']))
        else:
            erro = "Usuário ou senha inválidos."
    else:
        print("Formulário não validado:", form.errors)
    return render_template('login.html', form=form, erro=erro)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Formsignup()
    print("Método:", request.method)
    print("Dados recebidos:", request.form)
    if form.validate_on_submit():
        print("Formulário validado!")
        query = "INSERT INTO usuario (nome, username, email, senha) VALUES (%s, %s, %s, %s)"
        params = (form.nome.data, form.username.data, form.email.data, form.senha.data)
        execute_sql(query, params)
        print("Usuário inserido!")
        return redirect(url_for('views.home'))
    else:
        print("Formulário não validado:", form.errors)
    return render_template('signup.html', form=form)