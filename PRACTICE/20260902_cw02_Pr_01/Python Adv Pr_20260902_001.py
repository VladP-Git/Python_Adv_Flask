from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello Flask!</h1>'

@app.route('/user/<name>')
def user_profile(name):
    return f'<h1>Hello, {name}!</h1>'

if __name__ == '__main__':
    app.run()

