from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):
    id = StringField('Кого забанить', validators=[DataRequired()])
    submit = SubmitField('Бан')