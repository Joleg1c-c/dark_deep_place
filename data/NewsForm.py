from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, BooleanField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    # category = StringField('', validators=[DataRequired()])
    title = StringField('', validators=[DataRequired()])
    cost = StringField('', validators=[DataRequired()])
    content = TextAreaField("")
    is_private = BooleanField("Личное")
    submit = SubmitField('Разместить')