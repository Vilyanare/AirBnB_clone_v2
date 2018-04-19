#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /
    /hbnb
    /c/<text>
    /python/(<text>)
    /number/<n>
    /number_template/<n>
    /number_odd_or_even/<n>
'''
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def main():
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def C_text(text):
    return 'C {}'.format(text).replace('_', ' ')


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    return 'Python {}'.format(text).replace('_', ' ')


@app.route('/number/<int:n>')
def number_n(n):
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def odd_or_even(n):
    return render_template('6-number_odd_or_even.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
