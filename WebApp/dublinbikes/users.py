from dublinbikes.getdata import get_locations, get_current_station_data, get_all_station_data
import mysql.connector

def get_password(email):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('get_password', [email, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)


    for result in results:
        password = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return password




def add_user(email, password):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('add_user', (email, password, ))
        mydb.commit()

        print(mycursor.rowcount)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    mycursor.close()
    mydb.close()
    


def add_favourite_station(stations, user_id):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('add_station_to_user', (stations, user_id, ))
        mydb.commit()

        print(mycursor.rowcount)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    mycursor.close()
    mydb.close()
    

# def get_password(email):
#     pass

def get_favourite_stations(id):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('get_fav_stations_by_id', [id, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)


    for result in results:
        stations = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return stations


def check_email(email):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('check_if_email_exists', [email, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    for result in results:
        email_exists = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return email_exists


@login_manager.user_loader
def load_user(email):
    if(check_email(email)):
        return User(email)
    else:
        return None

class User():
    def __init__(self, email):
        try:
            # Connect to the RDS database
            mydb = mysql.connector.connect(
                host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
                user="admin",
                passwd="fmRdzKkP6mTtwEEsCByh",
                database="dublinbikes"
            )

            mycursor = mydb.cursor()

            # called mysql stored procedure giving email as an argument
            mycursor.callproc('get_user_details_by_email', [email, ])

            results = mycursor.stored_results()

        except mysql.connector.Error as err:

            print("SOMETHING WENT WRONG:", err)

        for result in results:
            u = result.fetchall()[0]
            self.id = u[0]
            self.email = u[1]
            self.password = u[2]
            self.stations = u[3]


        mycursor.close()
        mydb.close()

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.password}, {self.stations}"



# u = User("cshorttcd.ie")
# print(str(u))



load_user("cshort@tcd.ie")
