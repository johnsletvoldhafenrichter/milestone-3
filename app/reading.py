from flask import render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo, pymongo, DESCENDING

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS

@app.route('/')
def index():
    session['user_sort']=1
    session['rating_sort']=1
    session['game_sort']=1
    session['review_sort']=1
    return redirect(url_for('browse'))

@app.route('/all_games')
def all_games():
    return render_template('all_games.html',
                            gamelist=DB_GAME_LIST.find())

@app.route('/user_sort')
def user_sort():
    if session['user_sort'] == 1:
        session['user_sort']=-1
        session['rating_sort']=1
        session['game_sort']=1
        session['review_sort']=1
    else:
        session['user_sort'] = 1
    return redirect(url_for('browse'))

@app.route('/rating_sort')
def rating_sort():
    if session['rating_sort'] == 1:
        session['rating_sort']=-1
        session['user_sort']=1
        session['game_sort']=1
        session['review_sort']=1
    else:
        session['rating_sort'] = 1
    return redirect(url_for('browse'))

@app.route('/game_sort')
def game_sort():
    if session['game_sort'] == 1:
        session['game_sort']=-1
        session['rating_sort']=1
        session['user_sort']=1
        session['review_sort']=1
    else:
        session['game_sort'] = 1
    return redirect(url_for('browse'))

@app.route('/review_sort')
def review_sort():
    if session['review_sort'] == 1:
        session['review_sort']=-1
        session['rating_sort']=1
        session['game_sort']=1
        session['user_sort']=1
    else:
        session['review_sort'] = 1
    return redirect(url_for('browse'))

@app.route('/browse', methods=['POST', 'GET'])
def browse(): 
    if request.method == 'POST':
        game_json = request.form['game_select']
        browse_user=request.form['browse_user']
        browse_rating=request.form['browse_rating']

        if game_json != "":
            game_objects = game_json.split(',')
            game_name_slice_front = game_objects[1][10:]
            game_name = game_name_slice_front[:-1]
            game_pic_slice_front = game_objects[3][18:]
            game_pic = game_pic_slice_front[:-1]
            wiki_link_slice_front = game_objects[4][15:]
            wiki_link = wiki_link_slice_front[:-1]
            session['game_name']=game_name
            session['game_picture']=game_pic
            session['game_wiki_link']=wiki_link
            session['game_json']=game_json
        if browse_user != "":
            session['browse_user']=request.form['browse_user']
        if browse_rating != "":
            session['browse_rating']=int(request.form['browse_rating'])

        return render_template('browse.html',
                                review_ratings=DB_REVIEWS.find().sort('rating', session['rating_sort']),
                                review_users=DB_REVIEWS.find().sort('username', session['user_sort']),
                                review_games=DB_REVIEWS.find().sort('game_name', session['game_sort']),
                                review_latest=DB_REVIEWS.find().sort('_id', session['review_sort']),
                                users=DB_USERS.find(),
                                reviews=DB_REVIEWS.find(),
                                games=DB_GAME_LIST.find())
    return render_template('browse.html',
                            review_ratings=DB_REVIEWS.find().sort('rating', session['rating_sort']),
                            review_users=DB_REVIEWS.find().sort('username', session['user_sort']),
                            review_games=DB_REVIEWS.find().sort('game_name', session['game_sort']),
                            review_latest=DB_REVIEWS.find().sort('_id', session['review_sort']),
                            users=DB_USERS.find(),
                            reviews=DB_REVIEWS.find(),
                            games=DB_GAME_LIST.find())

@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=DB_REVIEWS.find({'username': session['username']}),
                                game_list=DB_GAME_LIST.find())
    return render_template('no_login.html')

@app.route('/top_games')
def top_games():
    return render_template('top_games.html')