import datetime as dt

import wtforms
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms import SelectField, FieldList
from wtforms.fields import EmailField
from wtforms.validators import DataRequired

from wtforms import widgets, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from models import db_session
from models.doctors import Doctor
from models.professions import Department

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Reception(FlaskForm):

    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).all()
    choices = []
    i = 0
    for elem in deps:
        choices.append((elem.id, elem.title))
        i += 1
    doctors = db_sess.query(Doctor).all()
    department = SelectField('Department', coerce=int, choices=choices, id="dep_id")
    choices = [[doc.id, f'{doc.surname} {doc.name[0]}.{doc.sec_name[0]}.', doc.profession] for doc in doctors]
    ch_out = []
    for c in choices:
        c[1] = '\t'.join([c[1], str(c[2])])
        ch_out.append(c[:2])
    ch_out.sort(key=lambda x: int(x[-1].split('\t')[-1]))
    doctors = SelectField('Doctor', coerce=int, choices=ch_out, id="doc_id")
    choices = []
    today = dt.datetime.now()
    for i in range(7):
        choices.append(today.strftime('%u %d %m'))
        today += dt.timedelta(days=1)
    full_choices = choices[:]
    day_of_weeks = {'1': 'ПН', '2': 'ВТ', '3': 'СР', '4': 'ЧТ', '5': 'ПТ', '6': 'СБ', '7': 'ВС'}
    months = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
              '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа', '09': 'сентября',
              '10': 'октября', '11': 'ноября', '12': 'декабря'}
    #choices = [f'{day_of_weeks[c.split()[0]]} {c.split()[1]} {months[c.split()[2]]}' for c in sorted(choices, key=lambda x: x.split()[0])]
    choices = ['25', '26', '27']
    rec_date = SelectField('Date', coerce=int, choices=choices, id="date_id")

    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Войти')
