from flask import Blueprint

auth = Blueprint('auth', __name__)
    
@auth.route('/login')
def login():
    return "Página de login"

@auth.route('/logout')
def logout():
    return "Página de logout"

@auth.route('/sign-up')
def sign_up():
    return "Página de cadastro"
