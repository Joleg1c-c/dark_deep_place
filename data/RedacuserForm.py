from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RedacuserForm(FlaskForm):
    img = FileField('')
    name = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    contacts = StringField('')
    checkbox1 = BooleanField('')
    contact1 = StringField('')
    checkbox2 = BooleanField('')
    contact2 = StringField('')
    checkbox3 = BooleanField('')
    contact3 = StringField('')
    checkbox4 = BooleanField('')
    contact4 = StringField('')
    checkbox5 = BooleanField('')
    contact5 = StringField('')
    checkbox6 = BooleanField('')
    contact6 = StringField('')
    old_password = PasswordField('', validators=[DataRequired()])
    password = PasswordField('')
    submit = SubmitField('Сохранить')
