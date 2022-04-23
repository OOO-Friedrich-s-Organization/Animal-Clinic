from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
import wtforms
from wtforms.validators import DataRequired


class Comment(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    # image = wtforms.FileField('Загрузить картинку')
    submit = SubmitField('Отправить')