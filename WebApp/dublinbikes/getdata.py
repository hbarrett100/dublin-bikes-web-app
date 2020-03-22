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
    # sql_statement = ("SELECT * " 
    #                 "FROM dynamicinfo " 
    #                 "WHERE `time` = (SELECT MAX(`time`) " 
    #                 "FROM dynamicinfo " 
    #                 f"WHERE `id` ={id}) "
    #                 f"AND `id` ={id}")
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()
        # mycursor.execute(sql_statement)
        mycursor.callproc('get_stand_info_by_id', [id, ])
        result = mycursor.stored_results()


        print(result)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    data = []
    # for row in mycursor:

    for result in mycursor.stored_results():
        # station = result.fetchall()
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