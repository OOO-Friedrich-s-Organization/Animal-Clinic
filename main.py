import os

import flask
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from flask import Flask, render_template, make_response, jsonify, url_for, request
# from flask_login import login_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from waitress import serve
import sqlite3
import sys
import shutil

from werkzeug.utils import redirect, secure_filename

from forms.comment import Comment
from forms.reception import Reception
from forms.registration import RegisterForm, LoginForm
from forms.savebut import SaveButton, SendButton
from models import db_session
from models.doctors import Doctor
from models.news import News
from models.prices import Price
from models.professions import Department
from models.timetable import Timetable
from models.users import User
from models.сomment import Comments

app = Flask(__name__)

UPLOAD_FOLDER = '/static/img/comments'

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@app.route('/build')
def building():
    return "<h1>Здесь строится ветеринарная клиника!</h1>" \
           '<img src="static/img/build.jpg")'\
           "alt='стройка идет' width='300' height='300'>" \
           "<h2>Мы будем по адресу ул.10 лет Октября, 41!</h2>"\
           '<img src="static/img/map.JPG")'\
           "alt='адрес' width='600' height='600'>"


@app.route('/reception')
def reception():
    if current_user.is_authenticated:
        fio = 'Штрахт М.Г.'
        db_name = "db/doctors.db"
        db_session.global_init(db_name)
        db_sess = db_session.create_session()

        doctor = db_sess.query(Doctor).all()
        #doctora = {}
        #for d in doctor:
       #     doctora[f'{d.surname} {d.name[0]}.{d.sec_name[0]}.'] = d.id
        #id = doctora[fio]
        #ttable = db_sess.query(Timetable).filter(Timetable.doc_id == id).first()
        #date = '3 27 04'
       # day_of_weeks = {'1': 'mon', '2': 'tue', '3': 'wed', '4': 'thu', '5': 'fri', '6': 'sat', '7': 'sun'}
        list_val = []
        # work_time = eval(f'ttable.{day_of_weeks[date[0]]}')
        #
        # if work_time != '-':
        #     time_from, time_to = work_time.split('-')
        #     time_from = time_from.split(':')
        #     while time_from != time_to.split(':'):
        #         list_val.append(':'.join(time_from))
        #         if time_from[1] == '30':
        #             time_from[0] = str(int(time_from[0]) + 1)
        #             time_from[1] = '00'
        #         else:
        #             time_from[1] = '30'

        doc_name = ''
        if request.args.get('doc_name') is not None:
            doc_name = request.args.get('doc_name')
            print(doc_name)

        form = Reception()
        doc_name = ''
        if (len(doc_name) != 0):
            list_val = [['14:00', True, False], ['14:30', True, False], ['15:00', True, False],
                        ['15:30', True, False],
                        ['16:00', True, False], ['16:30', True, False], ['17:00', False, False],
                        ['17:30', False, False]]
            res = make_response(render_template("appointment.html", form=form, title='Запись на прием',
                                                list_val=list_val, list_val_len=len(list_val)))
        else:
            list_val = [['10:00', True, False], ['10:30', True, True, '27 апреля 10:30'],
                        ['11:00', True, False], ['11:30', True, False],
                        ['12:00', True, False], ['12:30', True, False], ['13:00', False, False],
                        ['13:30', False, False]]
            res = make_response(render_template("appointment.html", form=form, title='Запись на прием',
                                                list_val=list_val, list_val_len=len(list_val)))
        return res
    else:
        return 'Вы не авторизованы!!!'


@app.route('/personal')
def doctors():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    doctors = db_sess.query(Doctor).all()
    specialties = {}
    for spec in db_sess.query(Department).all():
        specialties[spec.title] = list(filter(lambda x: x.profession == spec.id, doctors))
    res = make_response(render_template("personal.html", specialties=specialties, title='Сотрудники'))

    # print("doctor")
    return res


@app.route('/price')
def price():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    service = db_sess.query(Price).all()
    deps = db_sess.query(Department).all()
    last_id = deps[-1].id
    for dep in deps:
        if dep.id not in [14, 15, 16]:
            last_id += 1
            pr2 = Price()
            pr2.id = last_id
            pr2.title = 'Консультационный приём повторный (в течение 1-го месяца)'
            pr2.cost = 300
            pr2.dep_id = dep.id
            service.insert(0, pr2)
            pr1 = Price()
            pr1.id = last_id
            pr1.title = 'Консультационный приём'
            pr1.cost = 500
            pr1.dep_id = dep.id
            service.insert(0, pr1)
    res = make_response(render_template("price.html", service=service, specialties=deps, title='Прайс-Лист'))
    return res


@app.route('/timetable', methods=['GET', 'POST'])
@login_required
def timetable():
    if request.method == "GET":
        db_name = "db/doctors.db"
        db_session.global_init(db_name)
        db_sess = db_session.create_session()
        timetable_data = db_sess.query(Timetable).all()
        docs = db_sess.query(Doctor).all()
        deps = db_sess.query(Department).all()
        indexes = [1, 6, 12, 18]
        form = SaveButton()
        res = render_template("timetable.html", data=timetable_data, doctors=docs, deps=deps, indexes=indexes,
                              form=form, title='Расписание')
        return res
    if request.method == "POST":
        class Form(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)

            def get_directory(self):
                return QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")

        app = QApplication(sys.argv)
        ex = Form()
        directory = ex.get_directory()
        if directory:
            shutil.copy('static\docs\Timetable.xlsx', directory)

    return redirect('/timetable')


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if current_user.is_authenticated:
        form = Comment()
        if request.method == "POST":
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                # if 'file' not in request.files:
                #     return redirect(request.url)
                # file = request.files[form.image.data]
                # filename = secure_filename(file.filename)
                # сохраняем файл
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                com = Comments(
                    email=current_user.email,
                    content=form.content.data,
                    # image=form.image.data
                )
                db_sess.add(com)
                db_sess.commit()
                return redirect('/comments')
        return render_template('comment.html',
                               title='Оставить отзыв',
                               form=form
                               )
    else:
        return 'Вы не авторизированы!!!'


@app.route('/comments', methods=['GET', 'POST'])
def all_comments():
    form = SendButton()
    if request.method == "GET":
        db_name = "db/doctors.db"
        db_session.global_init(db_name)
        db_sess = db_session.create_session()
        comments = db_sess.query(Comments).all()
        users = db_sess.query(User).all()
        res = make_response(render_template("comments.html", comments=comments,
                                            users=users, form=form, title='Отзывы'))
        return res
    if request.method == "POST":
        return redirect('/comment')


@app.route('/')
def news():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    wall_news = db_sess.query(News).all()
    res = make_response(render_template("news.html", news=wall_news, title='Ветклиника "Дом Манула"'))
    return res


@app.route('/about_us')
def about_us():
    res = make_response(render_template("contacts.html", self_status='active', title='О нас'))
    return res


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_name = "db/doctors.db"
        db_session.global_init(db_name)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_name = "db/doctors.db"
        db_session.global_init(db_name)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/api/prices')
def get_prices():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    prices = db_sess.query(Price).all()
    departments = db_sess.query(Department).all()
    dct = {}
    for d in departments:
        dct[d.title] = []
        if d.id not in [14, 15, 16]:
            dct[d.title].append({'title': 'Консультационный приём',
                                 'cost': 500})
            dct[d.title].append({'title': 'Консультационный приём повторный (в течение 1-го месяца)',
                                 'cost': 300})
        for p in prices:
            if p.dep_id == d.id:
                dct[d.title].append({'title': p.title,
                                     'cost': p.cost})
    return jsonify(dct)


if __name__ == '__main__':
    app.register_blueprint(blueprint)
    #app.run(host='0.0.0.0', port=8080)
    port = int(os.environ.get('PORT', 33507))
    serve(app, host=args.host, port=port)
