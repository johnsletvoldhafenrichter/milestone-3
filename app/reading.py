from flask import render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo, pymongo, DESCENDING

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS

@app.route('/')
def index():
    return redirect(url_for('browse'))

@app.route('/all_games')
def all_games():
    return render_template('all_games.html',
                            gamelist=DB_GAME_LIST.find())

@app.route('/browse', methods=['POST', 'GET'])
def browse(): 
    if request.method == 'POST':
        game_json = request.form['game_select']
        browse_user=request.form['browse_user']
        browse_rating=request.form['browse_rating']
        if game_json is not "":
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
        if browse_user is not "":
            session['browse_user']=request.form['browse_user']
        if browse_rating is not "":
            session['browse_rating']=int(request.form['browse_rating'])
        
        return render_template('browse.html',
                                users=DB_USERS.find({'$query': {}, '$orderby': {'name' : 1}}),
                                review_ratings=DB_REVIEWS.find({ '$query': {}, '$orderby': {'rating': -1}}),
                                review_users=DB_REVIEWS.find({ '$query': {}, '$orderby': {'username': 1}}),
                                review_games=DB_REVIEWS.find({ '$query': {}, '$orderby': {'game_name': -1}}),
                                review_latest=DB_REVIEWS.find({ '$query': {}, '$orderby': {'_id': -1}}),
                                reviews=DB_REVIEWS.find(),
                                games=DB_GAME_LIST.find())
    return render_template('browse.html',
                            users=DB_USERS.find({'$query': {}, '$orderby': {'name' : 1}}),
                            review_ratings=DB_REVIEWS.find({ '$query': {}, '$orderby': {'rating': -1}}),
                            review_names=DB_REVIEWS.find({ '$query': {}, '$orderby': {'username': -1}}),
                            review_games=DB_REVIEWS.find({ '$query': {}, '$orderby': {'game_name': -1}}),
                            review_latest=DB_REVIEWS.find({ '$query': {}, '$orderby': {'_id': -1}}),
                            reviews=DB_REVIEWS.find(),
                            games=DB_GAME_LIST.find())

@app.route('/user_sort')
def user_sort():
    if session['user_sort'] == False:
        session['user_sort']=True
        return redirect(url_for('browse'))
    elif session['user_sort'] == True:
        session['user_sort']=False
        return redirect(url_for('browse'))
    else:
        session['user_sort']=True
        return redirect(url_for('browse'))

@app.route('/rating_sort')
def rating_sort():
    if session['rating_sort'] == False:
        session['rating_sort']=True
        return redirect(url_for('browse'))
    elif session['rating_sort'] == True:
        session['rating_sort']=False
        return redirect(url_for('browse'))
    else:
        session['rating_sort']=True
        return redirect(url_for('browse'))

@app.route('/game_sort')
def game_sort():
    if session['game_sort'] == False:
        session['game_sort']=True
        return redirect(url_for('browse'))
    elif session['game_sort'] == True:
        session['game_sort']=False
        return redirect(url_for('browse'))
    else:
        session['game_sort']=True
        return redirect(url_for('browse'))

@app.route('/review_latest')
def review_latest():
    if session['review_latest'] == False:
        session['review_latest']=True
        return redirect(url_for('browse'))
    elif session['review_latest'] == True:
        session['review_latest']=False
        return redirect(url_for('browse'))
    else:
        session['review_latest']=True
        return redirect(url_for('browse'))


@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=DB_REVIEWS.find({'username': session['username']}),
                                game_list=DB_GAME_LIST.find())
    return render_template('no_login.html')