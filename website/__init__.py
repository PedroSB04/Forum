from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

def create_app():    

    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'fjibguirehwgiuheriu'
    
    from .views import views
    from .auth import auth

    bcrypt = Bcrypt(app)
    Login_manager = LoginManager(app)
    Login_manager.login_view = 'auth.login'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app