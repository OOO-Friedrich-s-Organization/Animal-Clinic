from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class SaveButton(FlaskForm):
    save_but = SubmitField('Скачать')


class SendButton(FlaskForm):
    send_but = SubmitField('Оставить отзыв')
