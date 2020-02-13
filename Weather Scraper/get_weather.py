from datetime import datetime
import requests 
#import mysql.connector

def unix_to_date(d):
    """ Takes a unix timestamp as found in the dynamic data json and converts
    to date and time for MySQL """

    ts = int(d) / 1000
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API_KEY

r = requests.get(url = URL)
dublin_data = r.json()

for attribute in dublin_data:
    if isinstance(dublin_data[attribute], dict):
        for key in dublin_data[attribute]:
            print(key + ": ", dublin_data[attribute][key])
    else:
        print(attribute + ": ", dublin_data[attribute])