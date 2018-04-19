#!/usr/bin/python3
'''
    Runs a flask app that serves pages
    /hbnb_filters
'''
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


@app.route('/hbnb_filters')
def state_list():
    '''
        Renders an html page from template listed
    '''
    states = []
    cities = []
    amenities = []
    for k, v in storage.all("State").items():
        states.append(v)
    for k, v in storage.all("City").items():
        cities.append(v)
    for k, v in storage.all("Amenity").items():
        amenities.append(v)
    return render_template(
        '10-hbnb_filters.html', cities=cities,
        states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    '''
        Closes current session of my DB
    '''
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
