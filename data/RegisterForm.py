from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    img = FileField('')
    name = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    password_again = PasswordField('', validators=[DataRequired()])
    rules_agree = BooleanField('', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
