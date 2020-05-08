from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    img = FileField('')
    name = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    password_again = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
