import time
from datetime import datetime
import requests 
import mysql.connector

def unix_to_date(d):
    """ Takes a unix timestamp as found in the weather JSON and converts
    to date and time for database """

    ts = int(d)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def get_datetime():
    """ Gets unix timestamp from time module and converts it to date-time format for database """

    ts = int(time.time())
    return unix_to_date(ts)

def print_elements():
    """Prints elements of to scraped json file for analysis"""
    for attribute in dublin_data:
        if isinstance(dublin_data[attribute], dict):
            for key in dublin_data[attribute]:
                print(key + ": ", dublin_data[attribute][key])
        elif isinstance(dublin_data[attribute], list):
            for key in dublin_data[attribute][0]:
                print(key + ": ", dublin_data[attribute][0][key])
        else:
            print(attribute + ": ", dublin_data[attribute])
    print()

def get_weather():
    """Scrapes weather data from openweathermap.org"""
    
    API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
    URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API_KEY

    time = get_datetime()
    r = requests.get(url = URL)
    dublin_data = r.json()

    data_weather = (
        str(time),
        str(dublin_data['weather'][0]['id']),
        str(dublin_data['weather'][0]['main']),
        str(dublin_data['weather'][0]['description']),
        str(dublin_data['main']['temp']),
        str(dublin_data['main']['feels_like']),
        str(dublin_data['main']['temp_min']),
        str(dublin_data['main']['temp_max']),
        str(dublin_data['main']['pressure']),
        str(dublin_data['main']['humidity']),
        str(dublin_data['visibility']),
        str(dublin_data['wind']['speed']),
        str(dublin_data['wind']['deg']),
        str(dublin_data['clouds']['all']),
        str(unix_to_date(dublin_data['dt'])),
        str(unix_to_date(dublin_data['sys']['sunrise'])),
        str(unix_to_date(dublin_data['sys']['sunset'])),
        str(dublin_data['timezone']),
    )

    cnx = mysql.connector.connect(user='root', password='Doritos58',
                                    host='127.0.0.1',
                                    database='mydb'
    )

    cursor = cnx.cursor()

    add_weather = ("INSERT INTO weather "
                    "(time, weatherid, weathermain, "
                    "weatherdescription, temp, feels_like, temp_min, "
                    "temp_max, pressure, humidity, visibility, windspeed, "
                    "winddirection, clouds, dt, sunrise, sunset, "
                    "timezone) " 
                    "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(add_weather, data_weather)

    cnx.commit()
    
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    get_weather()