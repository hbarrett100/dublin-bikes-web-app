from flask import Flask, render_template, url_for


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

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', locationdata=get_locations())

@app.route('/about')
def about(): 
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
