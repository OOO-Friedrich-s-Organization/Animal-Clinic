from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def building():
    return "<h1>Здесь строится ветеринарная клиника!</h1>" \
           '<img src="static/build.jpg")'\
           "alt='стройка идет' width='300' height='300'>" \
           "<h2>Мы будем по адресу ул.10 лет Октября, 41!</h2>"\
           '<img src="static/map.JPG")'\
           "alt='адрес' width='300' height='300'>"


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
