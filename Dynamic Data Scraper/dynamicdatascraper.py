"""

This script scrapes the dynamic data available through the Dublin Bikes API
It then adds it to the RDS database
It is being run every 5 mins on an EC2 instance using cron
Its print output is being added to a trace file on the EC2 instance

"""

from datetime import datetime
import requests
import mysql.connector
import sys

def unix_to_date(d):
    """ Takes a unix timestamp as found in the dynamic data json and converts
    to date and time for MySQL """

    ts = int(d) / 1000
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


api_key = "fc31aed31ee8e2ae5c2a3f75172b9167873f1bc9"
URL = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=" + api_key

try:
# Make the get request
    r = requests.get(url=URL)
except requests.exceptions.RequestException as err:
    print("SOMETHING WENT WRONG:", err)
    exit(1)



station_data = r.json()

# Create empty array to store values
sql_values = []

# Format the data for the sql statement and append to sql_values
for station in station_data:
    sql_values.append((
        str(station["number"]),
        str(station["available_bike_stands"]),
        str(station["available_bikes"]),
        str(station["status"]),
        str(unix_to_date(station["last_update"])),
        str(station["banking"]),
        str(station["bonus"]),
        str(station["bike_stands"]),
        ))

sql_statement = ("INSERT IGNORE INTO `dublinbikes`.`dynamicinfo`"
                 " (`ID`, `availstands`, `availbikes`, `status`, `time`, `banking`, `bonus`, `numbikestands`)"
                 " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

try:   
    # Connect to the RDS database
    mydb = mysql.connector.connect(
        host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
        user="admin",
        passwd="fmRdzKkP6mTtwEEsCByh",
        database="dublinbikes"
    )

    mycursor = mydb.cursor()

    # executemany iterates through the tuples in sql_values array and applies the sql_statement to each tuple
    mycursor.executemany(sql_statement, sql_values)

    # Apply the changes to the server
    mydb.commit()

except mysql.connector.Error as err:

    print("SOMETHING WENT WRONG:", err)
    exit(1)

# Print the time and number of records inserted. 
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "- " + str(mycursor.rowcount) + " records inserted.")
