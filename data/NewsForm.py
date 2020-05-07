from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, BooleanField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    cost = StringField('Цена', validators=[DataRequired()])
    content = TextAreaField("Описание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Разместить')