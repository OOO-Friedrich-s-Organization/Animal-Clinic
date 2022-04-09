from flask import Flask, render_template, make_response
from waitress import serve
import sqlite3

from models import db_session
from models.doctors import Doctor
from models.professions import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# @app.route('/')
# @app.route('/build')
# def building():
#     return "<h1>Здесь строится ветеринарная клиника!</h1>" \
#            '<img src="static/img/build.jpg")'\
#            "alt='стройка идет' width='300' height='300'>" \
#            "<h2>Мы будем по адресу ул.10 лет Октября, 41!</h2>"\
#            '<img src="static/img/map.JPG")'\
#            "alt='адрес' width='600' height='600'>"


# @app.route('/personal')
@app.route('/')
def doctors():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    doctors = db_sess.query(Doctor).all()
    specialties = {}
    for spec in db_sess.query(Department).all():
        specialties[spec.title] = list(filter(lambda x: x.profession == spec.id, doctors))
    res = make_response(render_template("personal.html", specialties=specialties))
    return res


@app.route('/test')
def test():
    res = make_response(render_template("timetable.html"))
    return res


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=8080)
