#formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .database import execute_sql

class Formlogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_de_confirmacao = SubmitField("Fazer Login")

class Formsignup(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField("Confirmar Senha",validators=[DataRequired(), EqualTo('senha')])
    botao_de_confirmacao = SubmitField("Cadastrar")

    def validate_email(self, email):
        query = "SELECT id_usuario FROM usuario WHERE email = %s"
        resultado = execute_sql(query, (email.data,), fetch_one=True)
        if resultado:
            raise ValidationError("Esse e-mail já está em uso.")