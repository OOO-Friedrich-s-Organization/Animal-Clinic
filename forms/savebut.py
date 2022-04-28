from flask_wtf import FlaskForm
from wtforms import SubmitField


class SaveButton(FlaskForm):
    save_but = SubmitField('Скачать')


class SendButton(FlaskForm):
    send_but = SubmitField('Оставить отзыв')
