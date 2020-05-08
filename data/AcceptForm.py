from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AcceptForm(FlaskForm):
    check = StringField('', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')