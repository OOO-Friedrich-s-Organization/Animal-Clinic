from flask import Flask, render_template, make_response
# from flask_login import login_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from waitress import serve
import sqlite3

from werkzeug.utils import redirect

from forms.registration import RegisterForm, LoginForm
from models import db_session
from models.doctors import Doctor
from models.prices import Price
from models.professions import Department
from models.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@app.route('/build')
def building():
    return "<h1>Здесь строится ветеринарная клиника!</h1>" \
           '<img src="static/img/build.jpg")'\
           "alt='стройка идет' width='300' height='300'>" \
           "<h2>Мы будем по адресу ул.10 лет Октября, 41!</h2>"\
           '<img src="static/img/map.JPG")'\
           "alt='адрес' width='600' height='600'>"


@app.route('/personal')
def doctors():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    # print('da')
    #doctors = db_sess.query(Doctor)
    doctors = db_sess.query(Doctor).all()
    # for doc in doctors:
    #     print(doc.id)
    deps = db_sess.query(Department).all()
    # print(deps)
    res = make_response(render_template("personal.html", doctors=doctors, deps=deps))
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
    res = make_response(render_template("price.html", service=service, deps=deps))
    return res


@app.route('/contacts')
def contact():
    res = make_response(render_template("contacts.html"))
    return res


@app.route('/test')
def test():
    res = make_response(render_template("timetable.html"))
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
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=8080)