import os
from flask import Flask, render_template, redirect, request, url_for, request, session
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'game_reviews'
app.config["MONGO_URI"] = os.getenv('client', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/add_review')
def add_review():
    return render_template('add_review.html',
                            gamelist=mongo.db.game_list.find())

@app.route('/insert_review', methods=['POST'])
def insert_review():
    review = mongo.db.reviews
    review.insert({'username': session['username'], 'description': request.form['review'], 'rating': request.form['rating']})
    return redirect(url_for('your_reviews'))



@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=mongo.db.reviews.find({'username': session['username']}))
    return render_template('no_login.html')

@app.route('/browse_reviews')
def browse():
    return render_template('browse.html',
            reviews=mongo.db.reviews.find())

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user = mongo.db.users
        existing_user = user.find_one({'email': request.form['email']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            user.insert({'name': request.form['username'], 'password': hashpass, 'email': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('your_reviews'))
        return render_template('fail_sign_up.html')
    return render_template('sign_up.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = mongo.db.users
        login_user = user.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = login_user['name']
                return redirect(url_for('your_reviews'))
        return render_template('fail_login.html')
    return render_template('login.html')

@app.route('/')
def index():
    return redirect(url_for('browse'))

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)