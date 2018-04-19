#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /states/
    /states/<id>
'''
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


@app.route('/states')
@app.route('/states/<id>')
def state_list(id=None):
    '''
        Renders an html page from template listed
    '''
    states = []
    cities = []
    for k, v in storage.all().items():
        if id is not None and isinstance(id, str):
            if id in k:
                id = v
        if 'State' in k:
            states.append(v)
        if 'City' in k:
            cities.append(v)
    if isinstance(id, str):
        id = -1
    return render_template(
        '9-states.html', cities=cities, states=states, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    '''
        Closes current session of my DB
    '''
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
