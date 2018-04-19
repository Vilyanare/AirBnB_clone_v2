#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /
    /hbnb
    /c/<text>
    /python/(<text>)
'''
from flask import Flask
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
