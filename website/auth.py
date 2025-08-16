from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
from website.database import execute_sql
from website.forms import Formlogin, Formsignup
from website.models import Usuario

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Formlogin()
    if form.validate_on_submit():
        query = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        params = (form.email.data, form.senha.data)
        usuario = execute_sql(query, params, fetch_one=True)
        if usuario:
            usuario_obj = Usuario(**usuario)
            login_user(usuario_obj)
            return redirect(url_for('views.perfil', id_usuario=usuario['id_usuario']))
        else:
            return render_template('login.html', form=form, erro="Usuário ou senha inválidos.")
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Formsignup()
    if form.validate_on_submit():
        query = "INSERT INTO usuario (nome, username, email, senha) VALUES (%s, %s, %s, %s)"
        params = (form.nome.data, form.username.data, form.email.data, form.senha.data)
        execute_sql(query, params)
        return redirect(url_for('views.home'))
    return render_template('signup.html', form=form)