#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /states_list
'''
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/states_list')
def state_list():
    '''
        Renders an html page from template listed
    '''
    states = []
    for k, v in storage.all("State").items():
        if 'State' in k:
            states.append(v)
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def teardown_db(exception):
    '''
        Closes current session of my DB
    '''
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
