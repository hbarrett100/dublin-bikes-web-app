from flask import render_template, url_for, request
from dublinbikes import app
from dublinbikes.getdata import get_locations, get_current_station_data
import json

print(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', locationdata=get_locations())


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/query')
def query():
    id = request.args.get('id')
    station_info = json.dumps(get_current_station_data(id))
    return station_info