import wtforms
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms import SelectField, FieldList
from wtforms.fields import EmailField
from wtforms.validators import DataRequired

from models import db_session
from models.doctors import Doctor
from models.professions import Department


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
    # dep_but = SubmitField('')

    #test = wtforms.FieldList(wtforms.TextAreaField('Да'))
    # Required = ['1', '2', '3']
    #myChoices = 3# number of choices
    #test = SelectField(u'Field name', choices=myChoices)

    department = SelectField('Department', coerce=int, choices=choices, id="dep_id")
    # index = int(department.data)
    # print(department.choices[index][1])
    # print(index)
    doctors = SelectField('Doctor', coerce=int, choices=[(doc.id, f'{doc.surname} {doc.name[0]}.{doc.sec_name[0]}.')
                                                         for doc in doctors])

    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Войти')
