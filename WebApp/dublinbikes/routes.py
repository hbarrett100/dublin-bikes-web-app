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
    # get the argument from the get request
    id = request.args.get('id')
    # invoke function to run sql query and store results
    station_info = json.dumps(get_current_station_data(id))
    return station_info