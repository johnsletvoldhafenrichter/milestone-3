# Importing modules
import os
from dotenv import load_dotenv
from flask import (
    Flask, render_template, redirect, request, url_for, request, session)
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
import bcrypt
import json

# Declaring app name
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'game_reviews'
app.config["MONGO_URI"] = os.environ.get('client', 'mongodb://localhost')

# Config settings and environmental variables
admin_password = os.environ.get('admin_password')
admin_user = os.environ.get('admin_user')
admin_email = os.environ.get('admin_email')
app.secret_key = os.environ.get("SECRET", "randomstring")


mongo = PyMongo(app)

# creating database functions

@app.route('/add_game')
def add_game():
    if 'username' in session:
        return render_template('add_game.html')
    return render_template('no_login.html')
    

@app.route('/add_review')
def add_review():
    if 'username' in session:
        return render_template('add_review.html',
                                gamelist=mongo.db.game_list.find())
    return render_template('no_login.html')

@app.route('/insert_game', methods=['POST'])
def insert_game():
    game = mongo.db.game_list
    game.insert({'name': request.form['name'], 'publisher': request.form['name'], 'picture_link': request.form['picture_link'], 'wiki_link': request.form['wiki_link']})
    return redirect(url_for('admin_tab'))


@app.route('/insert_review', methods=['POST'])
def insert_review():
    review = mongo.db.reviews
    review.insert({'game_name': request.form['game_name'], 'username': session['username'], 'description': request.form['review'], 'rating': request.form['rating']})
    return redirect(url_for('your_reviews'))

# reading database functions
""" different pages for rendering items out of the database
for example for browsing all games that are currently in database or
browsing different reviews or only showing the logged in users reviews
"""

@app.route('/all_games')
def all_games():
    return render_template('all_games.html',
                            gamelist=mongo.db.game_list.find())

@app.route('/browse', methods=['POST', 'GET'])
def browse(): 
    if request.method == 'POST':
        game_json = request.form['game_select']
        game_objects = game_json.split(',')
        game_name_slice_front = game_objects[1][10:]
        game_name = game_name_slice_front[:-1]
        game_pic_slice_front = game_objects[3][18:]
        game_pic = game_pic_slice_front[:-1]
        
        return render_template('browse.html',
                                reviews=mongo.db.reviews.find(),
                                games=mongo.db.game_list.find(),
                                name=game_name,
                                picture=game_pic)
    return render_template('browse.html',
                            reviews=mongo.db.reviews.find(),
                            games=mongo.db.game_list.find())

@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=mongo.db.reviews.find({'username': session['username']}),
                                game_list=mongo.db.game_list.find())
    return render_template('no_login.html')

# updating database functions

@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    if session['admin']:
        game = mongo.db.game_list.find_one({"_id": ObjectId(game_id)})
        return render_template('edit_game.html',
                                game=game)
    return render_template('no_login.html')

@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    if session['admin']:
        games = mongo.db.game_list
        games.update( {'_id': ObjectId(game_id)},
        {
            'name':request.form.get('name'),
            'publisher':request.form.get('publisher'),
            'picture_link': request.form.get('picture_link'),
            'wiki_link': request.form.get('wiki_link'),
        })
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')


@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    if session['username']:
        review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        return render_template('edit_review.html',
                                review=review,
                                gamelist=mongo.db.game_list.find())
    return render_template('no_login.html')

@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    if session['username']:
        reviews = mongo.db.reviews
        reviews.update({'_id': ObjectId(review_id)},
        {
            'game_name':request.form.get('game_name'),
            'username': request.form.get('username'),
            'description': request.form.get('review'),
            'rating': request.form.get('rating'),
        })
        if session['admin']:
            return redirect(url_for('admin_tab'))
        return redirect(url_for('your_reviews'))
    return render_template('no_login.html')



@app.route('/edit_user/<user_id>')
def edit_user(user_id):
    if session['admin']:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return render_template('edit_user.html',
                                user=user)
    return render_template('no_login.html')

@app.route('/update_user/<user_id>/<user_name>', methods=["POST"])
def update_user(user_id, user_name):
    if session['admin']:
        existing_user_name = mongo.db.users.find_one({"name": user_name})
        if existing_user_name is None:
            user = mongo.db.users
            user.update({'_id': ObjectId(user_id)},
            { '$set': {
                'name':request.form.get('name'),
                'email': request.form.get('email')
            }})
            return redirect(url_for('admin_tab'))
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return "Username already in use!" + render_template('edit_user.html',
                                user=user)
    return render_template('no_login.html')




# deleting database functions

@app.route('/delete_game/<game_id>/<game_name>')
def delete_game(game_id, game_name):
    if session['admin']:
        mongo.db.reviews.remove({'game_name': game_name})
        mongo.db.game_list.remove({'_id': ObjectId(game_id)})
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')

@app.route('/delete_user/<user_id>/<review_name>')
def delete_user(user_id, review_name):
    if session['admin']:
        mongo.db.reviews.remove({'username': review_name})
        mongo.db.users.remove({'_id': ObjectId(user_id)})
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    if session['username']:
        mongo.db.reviews.remove({'_id': ObjectId(review_id)})
        if session['admin']:
            return redirect(url_for('admin_tab'))
        return redirect(url_for('your_reviews'))
    return render_template('no_login.html')


# Sign up and Login pages and authentication

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user = mongo.db.users
        existing_user = user.find_one({'email': request.form['email']})
        existing_username = user.find_one({'name': request.form['username']})
        
        if existing_user is None and existing_username is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            user.insert({'name': request.form['username'], 'password': hashpass, 'email': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('browse'))
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
                if (session['username'] == admin_user) and (request.form['password'] == admin_password):
                    session['admin'] = True
                    return redirect(url_for('admin_tab'))
                else:
                    session['admin'] = False
                return redirect(url_for('your_reviews'))
        return render_template('fail_login.html')
    return render_template('login.html')

# root access and home page
@app.route('/admin_tab')
def admin_tab():
    if session['admin']:
        return render_template('admin_tab.html',
                                gamelist=mongo.db.game_list.find(),
                                reviews=mongo.db.reviews.find(),
                                users=mongo.db.users.find())
    return render_template('no_login.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

# config/startup

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)