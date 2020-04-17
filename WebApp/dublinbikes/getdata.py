import mysql.connector
from dublinbikes.config import *


# Connect to the database using credential in the config file
def connect_to_db():
    mydb = mysql.connector.connect(
        host = database_config["host"],
        user = database_config["user"],
        passwd=  database_config["password"],
        database = database_config["database"]
    )
    return mydb


# Get all the static bike info from the db
# This is used to get the locations of the bike stations and place them on the map
def get_locations():
    sql_statement = ("select * FROM staticinfo")

    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()
        mycursor.execute(sql_statement)

        print(mycursor)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    data = []
    for row in mycursor:
       data.append({'id': row[0],
                    'name': row[2],
                    'lat': row[3],
                    'lon': row[4]})
    mycursor.close()
    mydb.close()

    return data



# Get the current availability information for a stations using its ID
def get_current_station_data(id):
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()
        # called mysql stored procedure giving id as an argument
        mycursor.callproc('get_stand_info_by_id', [id, ])
        result = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

# create empty array
    data = []

# iterate through results of mysql stored procedure and append to array
    for result in mycursor.stored_results():
        for row in result.fetchall():
            data.append({'id': row[0],
                            'availstands': row[1],
                            'availbikes': row[2],
                            'status': row[3],
                            'time': str(row[4]),
                            'banking': row[5],
                            'bonus': row[6],
                            'numbikestands': row[7],
                            })

    mycursor.close()
    mydb.close()

    return data



# Get the current availability information for all stations
def get_all_station_data():
    import mysql.connector
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()
        # called mysql stored procedure giving id as an argument
        mycursor.callproc('get_current_stand_info')
        result = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

# create empty array
    data = {}

# iterate through results of mysql stored procedure and append to array
    for result in mycursor.stored_results():
        for row in result.fetchall():
            data[row[0]] ={'availstands': row[1],
                         'availbikes': row[2],
                         'status': row[3],
                         'time': str(row[4]),
                         'banking': row[5],
                         'bonus': row[6],
                         'numbikestands': row[7]
                         }
    mycursor.close()
    mydb.close()

    return data


# Get the average availabilty per day for a station
def get_weekly_data(id):
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()
        # called mysql stored procedure giving id as an argument
        mycursor.callproc('get_avg_daily_availbikes_by_id', [id, ])
        result = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

# create empty array
    data = {'availbikes': [], 'availstands': []}

# iterate through results of mysql stored procedure and append to array
    for result in mycursor.stored_results():
        for row in result.fetchall():
            data['availbikes'].append(row[0])
            data['availstands'].append(row[1])

    mycursor.close()
    mydb.close()

    return data



# Get the average availabilty per hour for a station on a particular day of the week
def get_hourly_data_by_day(day, id):
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()
        # called mysql stored procedure giving id as an argument
        mycursor.callproc('get_avg_hourly_availbike_by_day_and_id', [day, id])
        result = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

# create empty array
    data = {'availbikes': [], 'availstands': []}

# iterate through results of mysql stored procedure and append to array
    for result in mycursor.stored_results():
        for row in result.fetchall():
            data['availbikes'].append(row[0])
            data['availstands'].append(row[1])

    mycursor.close()
    mydb.close()
    return data


# Unpickle the saved model files
def deserialise_models():
    import os
    import pickle

    dirname = os.path.dirname(__file__)

    IDs = [38, 16, 36, 12, 113, 45, 2, 34, 56, 44, 104, 89, 87, 9, 29, 88, 66,
       62, 57, 103, 77, 106, 32, 79, 17, 114, 102, 33, 27, 4, 7, 64, 41,
       84, 37, 49, 107, 22, 69, 58, 3, 100, 48, 83, 94, 11, 39, 75, 90,
       61, 13, 96, 91, 72, 101, 65, 6, 109, 55, 53, 115, 24, 112, 42, 73,
       30, 26, 92, 71, 93, 19, 97, 40, 15, 10, 28, 68, 31, 23, 99, 63, 98,
       8, 5, 86, 43, 110, 108, 50, 105, 76, 52, 74, 80, 59, 78, 117, 82,
       51, 85, 21, 81, 95, 18, 54, 111, 67, 47, 25]

    models = dict()
    for ID in IDs:
        #distinguish between windows/unix for describing file path
        if os.name == 'nt':
            filename = os.path.join(dirname, 'models\\model_'+str(ID)+'.pkl')
        else:
            filename = os.path.join(dirname, 'models/model_'+str(ID)+'.pkl')
        with open(filename,'rb') as handle:
            models[ID] = pickle.load(handle)
        # with open('C:\\Users\\Mesel\\Documents\\CS_Masters\\software_engineering\\dublin-bikes-app\\WebApp\\dublinbikes\\models\\model_'+str(ID)+'.pkl','rb') as handle:
        #     models[ID] = pickle.load(handle)
    return models


# Get the current 5 day forecast fron openweathermap API
def get_5day_forcast():
    import requests

    """Scrapes weather data from openweathermap.org"""
    
    API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
    URL = "http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&appid=" + API_KEY
    
#     time = get_datetime()
    try:
        r = requests.get(url = URL)
    except: 
        print("Scraping error: data not collected.")
        return None
    
    dublin_data = r.json()
    return dublin_data


# Make a dictionary of the predicted availabiltly of a station for the next 5 days
def get_prediction(stationid):
    import numpy as np
    import datetime
    import mysql.connector
    import simplejson as json
    import os

    stationid=int(stationid)

    #load json file containing numbikestands data
    dirname = os.path.dirname(__file__)
    if os.name == 'nt':
        filename = os.path.join(dirname, 'static\\station_numbikestands.json')
    else:
        filename = os.path.join(dirname, 'static/station_numbikestands.json')

    with open(filename,'r') as handle:
        station_numbikestands = json.load(handle)
    numbikestands = station_numbikestands[str(stationid)]

    weather_conditions = ['weatherid_300', 
                          'weatherid_301',
                          'weatherid_310', 
                          'weatherid_311', 
                          'weatherid_500', 
                          'weatherid_501', 
                          'weatherid_502', 
                          'weatherid_520', 
                          'weatherid_521', 
                          'weatherid_531', 
                          'weatherid_612', 
                          'weatherid_701', 
                          'weatherid_741', 
                          'weatherid_800', 
                          'weatherid_801', 
                          'weatherid_802', 
                          'weatherid_803', 
                          'weatherid_804', 
                         ]
    station_data = get_current_station_data(stationid)[0]
    
    dublin_data = get_5day_forcast()
    forecasts = dict()
    for prediction in dublin_data['list']:
        forecast = {
            'temp':prediction['main']['temp'],
            'feels_like':prediction['main']['feels_like'],
            'temp_min':prediction['main']['temp_min'],
            'temp_max':prediction['main']['temp_max'],
            'pressure':prediction['main']['pressure'],
            'humidity':prediction['main']['humidity'],
            'windspeed':prediction['wind']['speed'],
            'winddirection':prediction['wind']['deg'],
            'clouds':prediction['clouds']['all'],
            'sunrise':datetime.datetime.fromtimestamp(dublin_data['city']['sunrise']).hour,
            'sunset':datetime.datetime.fromtimestamp(dublin_data['city']['sunset']).hour,
            'hour':datetime.datetime.fromtimestamp(prediction['dt']).hour
        }
        if datetime.datetime.fromtimestamp(prediction['dt']).hour < 5:
            if datetime.datetime.fromtimestamp(prediction['dt']).hour == 0 and datetime.datetime.fromtimestamp(prediction['dt']).minute > 30:
                forecast['status_CLOSED'] = 1
                forecast['status_OPEN'] = 0
            elif datetime.datetime.fromtimestamp(prediction['dt']).hour > 0:
                forecast['status_CLOSED'] = 1
                forecast['status_OPEN'] = 0
            else:
                forecast['status_CLOSED'] = 0
                forecast['status_OPEN'] = 1
        else: 
            forecast['status_CLOSED'] = 0
            forecast['status_OPEN'] = 1
            
        if station_data['banking'] == 'False':
            forecast['banking_False'] = 1
            forecast['banking_True'] = 0
        elif station_data['banking'] == 'True':
            forecast['banking_False'] = 0
            forecast['banking_True'] = 1
        else:
            # default banking info in case database access fails
            forecast['banking_False'] = 1
            forecast['banking_True'] = 0

        for condition in weather_conditions:
            if 'weatherid_' + str(prediction['weather'][0]['id']) == condition:
                forecast[condition] = 1
            else:
                forecast[condition] = 0 
        for i in range(7):
            if datetime.datetime.fromtimestamp(prediction['dt']).weekday() == i:
                forecast['weekday_'+str(i)] = 1
            else:
                forecast['weekday_'+str(i)] = 0
        days_from_today = (datetime.datetime.fromtimestamp(prediction['dt']).date() - datetime.datetime.today().date()).days
        forecasts[(stationid,forecast['hour'],days_from_today)] = forecast

    models = deserialise_models()
    station = {
        0:dict(),
        1:dict(),
        2:dict(),
        3:dict(),
        4:dict(),
        5:dict()
    }
    for key in forecasts:
        for i in range(3):
            hour = key[1] + i
            day = key[2]
            if hour > 23:
                day += 1
                hour -= 24
            station[day][hour] = forecasts[key]
            station[day][hour]['hour'] = hour
            station[day][hour] = np.array([value for value in forecasts[key].values()])
            X = station[day][hour].reshape(1, -1) 
            y = models[stationid].predict(X)
            station[day][hour] = int(round(y[0]))
    station['numbikestands'] = numbikestands
    return station



# Get the forecast for a particular date and time from the 5 day forecast
def get_hourly_forecast(day,hour):
    import datetime
    import requests

    forecast = get_5day_forcast()
    weather = dict()
    for prediction in forecast['list']:
        for i in range(3):
            time = prediction['dt'] + 60*60*i
            days_from_today = (datetime.datetime.fromtimestamp(time).date() - datetime.datetime.today().date()).days
            if days_from_today == day:
                thishour = datetime.datetime.fromtimestamp(time).hour
                if thishour == hour:
                    weather['weatherdescription'] = prediction['weather'][0]['description']
                    weather['temp'] = int(round(prediction['main']['temp'] - 273.15))
                    weather['wind'] = int(round(prediction['wind']['speed']*3.6))
                    return weather

    API_KEY = "16fb93e92d3bd8aefd9b647c1a8f6acf"
    URL = "http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=" + API_KEY

    try:
        r = requests.get(url = URL)
    except: 
        return None

    current_weather = r.json()

    weather = {
        'weatherdescription':current_weather['weather'][0]['description'],
        'temp':int(round(current_weather['main']['temp'] - 273.15)),
        'wind':int(round(current_weather['wind']['speed']*3.6))
    }
    return weather
