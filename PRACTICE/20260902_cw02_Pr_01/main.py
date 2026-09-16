from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

@app.route('/<name>')
def user_profile(name):
    return f'<h1>Hello, {name}!</h1>'

@app.route('/<int:number>')
def duble_number(number):
    return jsonify({'return' : f' {number} dubled is {number * 2} </h1>'})

@app.route('/square/<float:number>')
def square_number(number):
    return jsonify({'result' : f'The square of {number} is {number * number}'})

@app.route('/reverse/<path:text>')
def reverse_text(text):
 return f'{text} reversed is {text[::-1]}'

if __name__ == '__main__':
    app.run(debug=True)

