from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from website.database import execute_sql
from website.models import Usuario  # Ajuste conforme seu modelo de usuário

login_manager = LoginManager()  # Crie aqui, fora da função

def create_app():    
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'fjibguirehwgiuheriu'
    
    from .views import views
    from .auth import auth

    bcrypt = Bcrypt(app)
    login_manager.init_app(app)  # Inicialize aqui
    login_manager.login_view = 'auth.login'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

# Defina o user_loader fora da função também
@login_manager.user_loader
def load_user(user_id):
    query = "SELECT * FROM usuario WHERE id_usuario = %s"
    usuario = execute_sql(query, (user_id,), fetch_one=True)
    if usuario:
        return Usuario(**usuario)
    return None