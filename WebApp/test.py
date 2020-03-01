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

    data = {}
    for row in mycursor:
        data[row[0]] = (row[3], row[4],)
    mycursor.close()
    mydb.close()

    return data

app = Flask(__name__)

posts = [
    { 
    'author': 'Conor',
    'title':'blog post 1',
    'content': 'First post content',
    'date_posted' : 'Feb 23, 2020'
    },

 { 'author': 'JiJi',
    'title':'blog post 2',
    'content': 'Seoncd post content',
    'date_posted' : 'Feb 23, 2020'
    }

]

locationdata = [1,2,3]
print(locationdata)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about(): 
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
