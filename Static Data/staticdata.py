import mysql.connector
import json
import os
import sys

file = os.path.join(sys.path[0], 'dublin.json')

# read json file
with open(file, 'r') as f:
    static_dict = json.load(f)

# create array of tuples containing information for each station
station_info = []
for station in static_dict: 
    t = (station["number"], station["name"], station["address"],station["latitude"], station["longitude"])
    station_info.append(t)

# connect to the database
try:
    mydb = mysql.connector.connect(
        host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
        user="admin",
        passwd="fmRdzKkP6mTtwEEsCByh",
        database="dublinbikes"
    )

except mysql.connector.Error as e:
    print("Error Code:", e)
    exit(1)
    

mycursor = mydb.cursor()

# insert the array of tuples into the table
sql = "INSERT INTO staticinfo (number, name, address, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"

# make changes to the server

try: 
    mycursor.executemany(sql, station_info)
    mydb.commit()
    
except mysql.connector.Error as err:
    print("Error:", err)
    exit(1)