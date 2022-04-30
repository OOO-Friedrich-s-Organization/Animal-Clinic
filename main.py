import flask
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from flask import Flask, render_template, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sys
import shutil

from werkzeug.utils import redirect

from forms.comment import Comment
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

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@app.route('/note')
def note():
    return render_template('reception.html')


@app.route('/personal')
def doctors():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    doctors = db_sess.query(Doctor).all()
    specialties = {}
    for spec in db_sess.query(Department).all():
        specialties[spec.title] = list(filter(lambda x: x.profession == spec.id, doctors))
    res = make_response(render_template("personal.html", specialties=specialties, title='Сотрудники',
                                        crew_status='my_active'))
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
    res = make_response(render_template("price.html", service=service, specialties=deps, title='Прайс-Лист',
                                        price_status='my_active'))
    return res


@app.route('/timetable', methods=['GET', 'POST'])
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
                              form=form, title='Расписание', time_status='my_active')
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
                com = Comments(
                    email=current_user.email,
                    content=form.content.data,
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
                                            users=users, form=form, title='Отзывы', reviews_status='my_active'))
        return res
    if request.method == "POST":
        return redirect('/comment')


@app.route('/')
def news():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    wall_news = db_sess.query(News).all()
    res = make_response(render_template("news.html", news=wall_news[::-1], title='Ветклиника "Дом Манула"',
                                        main_status='my_active'))
    return res


@app.route('/about_us')
def about_us():
    res = make_response(render_template("contacts.html", self_status='my_active', title='О нас'))
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
    app.run(host='0.0.0.0', port=5000)
