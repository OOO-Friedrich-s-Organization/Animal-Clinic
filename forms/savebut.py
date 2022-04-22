from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class SaveButton(FlaskForm):
    save_but = SubmitField('Скачать')
    #, render_kw={"onclick": "timetable()"}
    # save_but.