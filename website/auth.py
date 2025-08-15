from flask import Blueprint, render_template, redirect, url_for
from website.database import execute_sql
from website.forms import Formlogin, Formsignup

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Formlogin()
    if form.validate_on_submit():
        query = "INSERT INTO usuario (email, senha) VALUES (%s, %s)"
        params = (form.email.data, form.senha.data)
        execute_sql(query, params) 
        return redirect(url_for('views.perfil'))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Formsignup()
    if form.validate_on_submit():
        query = "INSERT INTO usuario (nome, username, email, senha) VALUES (%s, %s, %s, %s)"
        params = (form.nome.data, form.username.data, form.email.data, form.senha.data)
        execute_sql(query, params)
        return redirect(url_for('views.home'))
    return render_template('signup.html', form=form)    