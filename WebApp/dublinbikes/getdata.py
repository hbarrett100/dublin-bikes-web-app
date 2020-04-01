def get_locations():
    import mysql.connector
    sql_statement = ("select * FROM staticinfo")

    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

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


def get_current_station_data(id):
    import mysql.connector
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

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


def get_all_station_data():
    import mysql.connector
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

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

def get_model_predictions():
    import mysql.connector
    try:
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )
        mycursor = mydb.cursor()
        
        mycursor.callproc('get_predictions')
        result = mycursor.stored_results()
        
    except mysql.connector.Error as err:
        print("SOMETHING WENT WRONG:", err)
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals():
            mydb.close()
        exit(1)
        
    data = {}
    for result in mycursor.stored_results():
        stationid = None
        for row in result.fetchall():
            if row[0] != stationid:
                stationid = row[0]
                data[stationid] = dict()
                data[stationid]['hour'] = []
                data[stationid]['availbikes'] = []
                data[stationid]['availstands'] = []
                data[stationid]['hour'] += [row[1]]
            data[stationid]['availbikes'] += [row[2]]
            data[stationid]['availstands'] += [row[3]]
    mycursor.close()
    mydb.close()
    
    return data
