from flask import Flask, render_template, make_response
from waitress import serve
import sqlite3

from models import db_session
from models.doctors import Doctor
from models.prices import Price
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


@app.route('/personal')
def doctors():
    db_name = "db/doctors.db"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    doctors = db_sess.query(Doctor).all()
    specialties = {}
    for spec in db_sess.query(Department).all():
        specialties[spec.title] = list(filter(lambda x: x.profession == spec.id, doctors))
    res = make_response(render_template("personal.html", specialties=specialties, crew_status='active'))
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
    res = make_response(render_template("price.html", service=service, specialties=deps, price_status='active'))
    return res


@app.route('/about_us')
def contact():
    res = make_response(render_template("contacts.html", self_status='active'))
    return res


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=8080)
