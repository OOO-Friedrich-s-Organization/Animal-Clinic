from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def building():
    return "<html>Здесь строится ветеринарная клиника!<html>" \
           '<img src="static/build.jpg")'\
           "alt='стройка идет' width='300' height='300'>"


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
