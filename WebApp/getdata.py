

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
       data.append({'id': [row[0]],
                    'lat' : row[3],
                    'lon' : row[4]})
    mycursor.close()
    mydb.close()

    return data

get_locations()
