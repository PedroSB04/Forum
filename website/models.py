# filepath: c:\Users\enzop\OneDrive\Documentos\ufop\Forum\website\models.py
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nome, username, email, senha, **kwargs):
        self.id = id_usuario
        self.nome = nome
        self.username = username
        self.email = email
        self.senha = senha

    def get_id(self):
        return str(self.id)