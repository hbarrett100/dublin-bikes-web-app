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
    try:
        r = requests.get(url = URL)
    except: 
        print("Scraping error: data not collected.")
        exit(1)
    
    dublin_data = r.json()

    data_weather = (
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
    add_weather = ("INSERT INTO dynamicweather "
                    "(weatherid, weathermain, "
                    "weatherdescription, temp, feels_like, temp_min, "
                    "temp_max, pressure, humidity, visibility, windspeed, "
                    "winddirection, clouds, dt, sunrise, sunset, "
                    "timezone) " 
                    "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    try:
        cnx = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )   
        cursor = cnx.cursor()
        cursor.execute(add_weather, data_weather)
        cnx.commit()
        print("Row added.")
        cursor.close()
        cnx.close()
    except: 
        print("Database error: row not added.")
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()
        exit(1)

if __name__ == "__main__":
    get_weather()