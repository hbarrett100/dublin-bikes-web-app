import mysql.connector
import json

# read json file
with open('/Users/hannahbarrett/Documents/CompScience/Semester2/30830softeng/Project/dublin.json', 'r') as f:
    static_dict = json.load(f)

# create array of tuples containing information for each station
station_info = []
for station in static_dict: 
    t = (station["number"], station["name"], station["address"],station["latitude"], station["longitude"])
    station_info.append(t)

# connect to the database
mydb = mysql.connector.connect(
  host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
  user="admin",
  passwd="fmRdzKkP6mTtwEEsCByh",
  database="dublinbikes"
)

mycursor = mydb.cursor()

# insert the array of tuples into the table
sql = "INSERT INTO staticinfo (number, name, address, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"

mycursor.executemany(sql, station_info)

# make changes to the server
mydb.commit()
