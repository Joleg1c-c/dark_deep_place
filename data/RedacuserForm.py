from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RedacuserForm(FlaskForm):
    img = FileField('')
    name = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    contacts = StringField('', validators=[DataRequired()])
    old_password = PasswordField('', validators=[DataRequired()])
    password = PasswordField('')
    submit = SubmitField('Сохранить')
