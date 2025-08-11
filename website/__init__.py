from flask import Flask
import os



def create_app():

    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'), template_folder=os.path.join(base_dir, 'templates'))
    app.config['SECRET_KEY'] = 'fjibguirehwgiuheriu'
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app