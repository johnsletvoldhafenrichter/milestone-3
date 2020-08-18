from flask import render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo, pymongo, DESCENDING
import math

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS, DB_COUNTER

@app.route('/')
def index():
    session['user_sort']=1
    session['rating_sort']=1
    session['game_sort']=1
    session['review_sort']=1
    session['TOTAL_PAGES'] = 0
    session['LIMIT'] = int(5)
    session['SKIP'] = 0
    session['PAGE_NUMBER'] = 0
    latest_reviews = DB_REVIEWS.find().sort('reviews_id', -1).limit(6)
    num_count=DB_COUNTER.find_one({'counter_name': 'counter'})
    games=num_count['number_games']
    reviews=num_count['number_reviews']
    users=num_count['number_users']
    return render_template('index.html',
                            lates_reviews=latest_reviews,
                            games=games,
                            reviews=reviews,
                            users=users)

# Pagination

@app.route('/page_count/<num>')
def page_count(num):
    session['PAGE_NUMBER'] = int(num)
    if session['PAGE_NUMBER'] < 0:
        session['PAGE_NUMBER'] = 0
    elif session['PAGE_NUMBER'] >= session['TOTAL_PAGES']:
        session['PAGE_NUMBER'] = session['TOTAL_PAGES']
    session['SKIP'] = int(session['PAGE_NUMBER']*session['LIMIT'])
    return redirect(url_for('browse') + '#sorting')

@app.route('/change_limit/<num>')
def change_limit(num):
    session['LIMIT'] = int(num)
    return redirect(url_for('browse') + '#sorting')


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
    return redirect(url_for('browse') + '#sorting')

@app.route('/rating_sort')
def rating_sort():
    if session['rating_sort'] == 1:
        session['rating_sort']=-1
        session['user_sort']=1
        session['game_sort']=1
        session['review_sort']=1
    else:
        session['rating_sort'] = 1
    return redirect(url_for('browse') + '#sorting')

@app.route('/game_sort')
def game_sort():
    if session['game_sort'] == 1:
        session['game_sort']=-1
        session['rating_sort']=1
        session['user_sort']=1
        session['review_sort']=1
    else:
        session['game_sort'] = 1
    return redirect(url_for('browse') + '#sorting')

@app.route('/review_sort')
def review_sort():
    if session['review_sort'] == 1:
        session['review_sort']=-1
        session['rating_sort']=1
        session['game_sort']=1
        session['user_sort']=1
    else:
        session['review_sort'] = 1
    return redirect(url_for('browse') + '#sorting')

@app.route('/browse', methods=['POST', 'GET'])
def browse():
    skip_limit = DB_REVIEWS.find().skip(session['SKIP']).limit(session['LIMIT'])
    review_ratings=skip_limit.sort('rating', session['rating_sort'])
    review_users=skip_limit.sort('username', session['user_sort'])
    review_games=skip_limit.sort('game_name', session['game_sort'])
    review_latest=skip_limit.sort('review_id', session['review_sort'])

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
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                users=DB_USERS.find(),
                                reviews=DB_REVIEWS.find().sort('reviews_id', -1).skip(session['SKIP']).limit(session['LIMIT']),
                                games=DB_GAME_LIST.find().sort('game_id', -1),
                                pages=session['TOTAL_PAGES'],
                                PAGE_NUMBER=session['PAGE_NUMBER'])

    return render_template('browse.html',
                            review_ratings=review_ratings,
                            review_users=review_users,
                            review_games=review_games,
                            review_latest=review_latest,
                            users=DB_USERS.find(),
                            reviews=DB_REVIEWS.find().sort('reviews_id', -1).skip(session['SKIP']).limit(session['LIMIT']),
                            games=DB_GAME_LIST.find().sort('game_id', -1),
                            pages=session['TOTAL_PAGES'],
                            PAGE_NUMBER=session['PAGE_NUMBER'])

@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=DB_REVIEWS.find({'username': session['username']}),
                                game_list=DB_GAME_LIST.find())
    return render_template('no_login.html')

@app.route('/top_games')
def top_games():
    total_ratings = DB_REVIEWS.aggregate([{'$group': {'_id': '$game_name', 'count': {'$sum': '$rating'}}}])
    total_reviews = DB_REVIEWS.aggregate([{'$group': {'_id': '$game_name', 'count': {'$sum': 1}}}])
    grp_average = DB_GAME_LIST.aggregate([{'$group': {'_id': '$name', 'avgAmount': {'$avg': { '$divide': ['$total_rating', '$total_reviews']}}}}])
    for rating in total_ratings:
        DB_GAME_LIST.update({'name': rating['_id']}, {'$set':{'total_rating': rating['count']}})
    for review in total_reviews:
        DB_GAME_LIST.update({'name': review['_id']}, {'$set':{'total_reviews': review['count']}})
    for grp in grp_average:
        if grp['avgAmount'] == None:
            continue
        average = round(grp['avgAmount'], 2)
        DB_GAME_LIST.update({'name': grp['_id']}, {'$set':{'average': average}})
        
    return render_template('top_games.html')