from flask import Flask, render_template, url_for
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

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about(): 
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)