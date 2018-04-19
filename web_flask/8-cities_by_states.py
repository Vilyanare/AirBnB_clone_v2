#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /cities_by_states
'''
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

@app.route('/cities_by_states')
def cities_by_states():
    '''
        Renders an html page from template listed
    '''
    states = []
    cities = []
    for k, v in storage.all().items():
        if 'State' in k:
            states.append(v)
        if 'City' in k:
            cities.append(v)
    return render_template('8-cities_by_states.html', trim_blocks=True, states=states, cities=cities,)

@app.teardown_appcontext
def teardown_db(exception):
    '''
        Closes current session of my DB
    '''
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
