from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class RedacNewsForm(FlaskForm):
    category = StringField('')
    title = StringField('', validators=[DataRequired()])
    cost = StringField('', validators=[DataRequired()])
    content = TextAreaField("", validators=[DataRequired()])
    imgs = IntegerField("")
    select_imgs = FileField('Выбрать изображения',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')],
                            render_kw={'multiple': True})
    submit = SubmitField('Разместить')
