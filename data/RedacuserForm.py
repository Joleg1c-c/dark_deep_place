from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RedacuserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    # img = FileField('Фотография', validators=[FileRequired()])
    contacts = StringField("контакты", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль')

    submit = SubmitField('Применить')
