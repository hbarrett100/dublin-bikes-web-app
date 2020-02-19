import time
from datetime import datetime
import requests 
import mysql.connector

def get_datetime():
    """ Gets unix timestamp from time module and converts it to date-time format for database """

    ts = int(time.time())
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def print_elements():
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
    API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
    URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API_KEY

    time = get_datetime()
    r = requests.get(url = URL)
    dublin_data = r.json()

    data_weather = (
        str(time),
        str(dublin_data['coord']['lon']),
        str(dublin_data['coord']['lat']),
        str(dublin_data['weather'][0]['id']),
        str(dublin_data['weather'][0]['main']),
        str(dublin_data['weather'][0]['description']),
        str(dublin_data['base']),
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
        str(dublin_data['dt']),
        str(dublin_data['sys']['type']),
        str(dublin_data['sys']['sunrise']),
        str(dublin_data['sys']['sunset']),
        str(dublin_data['timezone']),
        str(dublin_data['cod'])
    )

    cnx = mysql.connector.connect(user='root', password='Doritos58',
                                    host='127.0.0.1',
                                    database='mydb'
    )

    cursor = cnx.cursor()

    add_weather = ("INSERT INTO weather "
                    "(time, longitude, latitude, weatherid, weathermain, "
                    "weatherdescription, base, temp, feels_like, temp_min, "
                    "temp_max, pressure, humidity, visibility, windspeed, "
                    "winddirection, clouds, dt, type, sunrise, sunset, "
                    "timezone, cod) " 
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data_applicant = (711899, 'Antonio', 'Bandarez', 'His House', 881991)

    cursor.execute(add_weather, data_weather)

    cnx.commit()
    
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    get_weather()