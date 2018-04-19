#!/usr/bin/python3
'''
    Starts a flask application that servers / and /hbnb
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
