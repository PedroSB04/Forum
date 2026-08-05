# filepath: c:\Users\enzop\OneDrive\Documentos\ufop\Forum\website\models.py
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nome, username, email, senha, foto_perfil=None, **kwargs):
        self.id = id_usuario  # Necessário para Flask-Login
        self.id_usuario = id_usuario  # Necessário para seu código
        self.nome = nome
        self.username = username
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil

    def get_id(self):
        return str(self.id)