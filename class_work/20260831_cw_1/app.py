from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'First page of MyCafe'

@app.route('/menu')
def menu():
    return 'Menu of MyCafe'

@app.route('/events')
def events():
    return 'Events of MyCafe'


if __name__ == '__main__':
    app.run()