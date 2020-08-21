from flask import render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo, pymongo, DESCENDING
import math
import json
from app import app
from app.setup import (
                        DB_GAME_LIST,
                        DB_REVIEWS,
                        DB_USERS,
                        DB_COUNTER,
                        DB_GAME_SUGGESTION)


# index and initialization of all needed sessions
@app.route('/')
def index():
    session['LIMIT'] = int(6)
    session['TOTAL_PAGES'] = math.ceil(
        DB_REVIEWS.find().count()/session['LIMIT'])
    session['SKIP'] = 0
    session['PAGE_NUMBER'] = 1
    # sorting initialization
    session['user_sort'] = False
    session['rating_sort'] = False
    session['game_sort'] = False
    session['review_sort'] = False
    session['browse_user'] = False
    session['browse_rating'] = False
    session['game_name'] = False
    latest_reviews = DB_REVIEWS.find().sort(
        'review_id', -1
        ).limit(6)
    num_count = DB_COUNTER.find_one({'counter_name': 'counter'})
    games = num_count['number_games']
    reviews = num_count['number_reviews']
    users = num_count['number_users']
    return render_template(
                            'index.html',
                            lates_reviews=latest_reviews,
                            games=games,
                            reviews=reviews,
                            users=users)


# Pagination
# changing amount of pages, what to skip and change the shown results
# num = PAGE_NUMBER (reset to 1 by function redirecting to this, change_limit()
# where = variable declared by template
# to redirect back from where pagination was initiated on)
@app.route('/page_count/<num>/<where>')
def page_count(num, where):
    if where == 'browse' or where == 'your_reviews' or where == 'admin_tab_reviews':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(
            DB_REVIEWS.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int(
            (session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for(where))
    elif where == 'all_games' or where == 'admin_tab_games':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(
            DB_GAME_LIST.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for(where))
    elif where == 'admin_tab_users':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(
            DB_USERS.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for(where))
    elif where == 'admin_tab_suggestions':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(
            DB_GAME_SUGGESTION.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for(where))


# change the amount of results shown on page
@app.route('/change_limit/<num>/<where>')
def change_limit(num, where):
    if where:
        session['LIMIT'] = int(num)
        return redirect(url_for('page_count', num=1, where=where))


# rendering template for all games
@app.route('/all_games')
def all_games():
    gamelist = DB_GAME_LIST.find().sort(
        'name', 1).skip(
            session['SKIP']).limit(session['LIMIT'])
    results = DB_GAME_LIST.find().count()
    pages = math.ceil(
        DB_GAME_LIST.find().count()/session['LIMIT'])
    return render_template(
                            'all_games.html',
                            gamelist=gamelist,
                            pages=pages,
                            results=results,
                            PAGE_NUMBER=session['PAGE_NUMBER'])


# sorting the results, used by browse
@app.route('/sorting/<el>')
def sorting(el):
    if el == 'user':
        if session['user_sort'] == 1:
            session['user_sort'] = -1
            session['rating_sort'] = False
            session['game_sort'] = False
            session['review_sort'] = False
        else:
            session['user_sort'] = 1
            session['rating_sort'] = False
            session['game_sort'] = False
            session['review_sort'] = False
    elif el == 'rating':
        if session['rating_sort'] == 1:
            session['rating_sort'] = -1
            session['user_sort'] = False
            session['game_sort'] = False
            session['review_sort'] = False
        else:
            session['rating_sort'] = 1
            session['user_sort'] = False
            session['game_sort'] = False
            session['review_sort'] = False
    elif el == 'game':
        if session['game_sort'] == 1:
            session['game_sort'] = -1
            session['rating_sort'] = False
            session['user_sort'] = False
            session['review_sort'] = False
        else:
            session['game_sort'] = 1
            session['rating_sort'] = False
            session['user_sort'] = False
            session['review_sort'] = False
    elif el == 'latest':
        if session['review_sort'] == 1:
            session['review_sort'] = -1
            session['rating_sort'] = False
            session['game_sort'] = False
            session['user_sort'] = False
        else:
            session['review_sort'] = 1
            session['rating_sort'] = False
            session['game_sort'] = False
            session['user_sort'] = False
    return redirect(url_for('browse') + '#sorting')


# rendering template for main search in database,
# shows information of all databases except game_suggestions
@app.route('/browse', methods=['POST', 'GET'])
def browse():
    # initialization of required standard variables
    # required to show results and pagination without choosing choices
    review_ratings_sort = DB_REVIEWS.find().sort(
        'rating', session['rating_sort'])
    review_users_sort = DB_REVIEWS.find().sort(
        'username', session['user_sort'])
    review_games_sort = DB_REVIEWS.find().sort(
        'game_name', session['game_sort'])
    review_latest_sort = DB_REVIEWS.find().sort(
        'review_id', session['review_sort'])
    pages = math.ceil(
        DB_REVIEWS.find().count()/session['LIMIT'])
    all_reviews = DB_REVIEWS.find().skip(
        session['SKIP']).limit(session['LIMIT'])
    results = DB_REVIEWS.find().count()
    review_ratings = review_ratings_sort.skip(
        session['SKIP']).limit(session['LIMIT'])
    review_users = review_users_sort.skip(
        session['SKIP']).limit(session['LIMIT'])
    review_games = review_games_sort.skip(
        session['SKIP']).limit(session['LIMIT'])
    review_latest = review_latest_sort.skip(
        session['SKIP']).limit(session['LIMIT'])
    users = DB_USERS.find().sort('name', 1)
    games = DB_GAME_LIST.find().sort('name', 1)
    # sets variables when search query is made in browse form
    # redirects back to browse() in order to show results
    if request.method == 'POST':
        session['PAGE_NUMBER'] = 1
        game_json = request.form['game_select']
        browse_user = request.form['browse_user']
        browse_rating = request.form['browse_rating']
        if game_json != "":
            game_objects = game_json.split(',')
            game_name_slice_front = game_objects[1][10:]
            game_name = game_name_slice_front[:-1]
            game = DB_GAME_LIST.find_one({'name': game_name})
            session['game_name'] = game['name']
            session['game_picture'] = game['picture_link']
            session['game_wiki_link'] = game['wiki_link']
            session['game_description'] = game['game_description']
            session['game_average'] = game['average']
            session['game_json'] = game_json
        if browse_user != "":
            session['browse_user'] = request.form['browse_user']
        if browse_rating != "":
            session['browse_rating'] = int(
                request.form['browse_rating'])
        return redirect(url_for('browse'))
    # render template with all choices in browse form chosen
    if session['browse_user'] and session['game_name'] and session['browse_rating']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name'],
                'rating': session['browse_rating']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name'],
                'rating': session['browse_rating']})
        pages = math.ceil(
            DB_REVIEWS.find(
                {
                    'username': session['browse_user'],
                    'game_name': session['game_name'],
                    'rating': session['browse_rating']
                    }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name'],
                'rating': session['browse_rating']
                }).count()
        review_users = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_ratings = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                            'browse.html',
                            review_ratings=review_ratings,
                            review_users=review_users,
                            review_games=review_games,
                            review_latest=review_latest,
                            all_reviews=all_reviews,
                            users=users,
                            games=games,
                            pages=pages,
                            results=results,
                            PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with user and rating chosen in browse form
    elif session['browse_user'] and session['browse_rating']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'rating': session['browse_rating']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'rating': session['browse_rating']
                }).sort(
                    'game_name', session['game_sort'])
        review_games = review_games_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'rating': session['browse_rating']
                })
        pages = math.ceil(
            DB_REVIEWS.find(
                {
                    'username': session['browse_user'],
                    'rating': session['browse_rating']
                    }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'rating': session['browse_rating']
                }).count()
        review_users = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with user and game chosen in browse form
    elif session['browse_user'] and session['game_name']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_ratings_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name']
                }).sort(
                    'rating', session['rating_sort'])
        review_ratings = review_ratings_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name']
                })
        pages = math.ceil(
            DB_REVIEWS.find(
                {
                    'username': session['browse_user'],
                    'game_name': session['game_name']
                    }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'username': session['browse_user'],
                'game_name': session['game_name']
                }).count()
        review_users = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with rating and game chosen in browse form
    elif session['browse_rating'] and session['game_name']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'rating': session['browse_rating'],
                'game_name': session['game_name']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_users_sort = DB_REVIEWS.find(
            {
                'rating': session['browse_rating'],
                'game_name': session['game_name']
                }).sort(
                    'username', session['user_sort'])
        review_users = review_users_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'rating': session['browse_rating'],
                'game_name': session['game_name']})
        pages = math.ceil(DB_REVIEWS.find(
                {
                    'rating': session['browse_rating'],
                    'game_name': session['game_name']
                    }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'rating': session['browse_rating'],
                'game_name': session['game_name']
                }).count()
        review_ratings = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with user chosen in browse form
    elif session['browse_user']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_ratings_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user']
                }).sort(
                    'rating', session['rating_sort'])
        review_ratings = review_ratings_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games_sort = DB_REVIEWS.find(
            {
                'username': session['browse_user']
                }).sort(
                    'game_name', session['game_sort'])
        review_games = review_games_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'username': session['browse_user']})
        pages = math.ceil(
            DB_REVIEWS.find(
                {
                    'username': session['browse_user']
                    }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'username': session['browse_user']
                }).count()
        review_users = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with rating chosen in browse form
    elif session['browse_rating']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'rating': session['browse_rating']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_users_sort = DB_REVIEWS.find(
            {
                'rating': session['browse_rating']
                }).sort(
                    'username', session['user_sort'])
        review_users = review_users_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_games_sort = DB_REVIEWS.find(
            {
                'rating': session['browse_rating']
                }).sort(
                    'game_name', session['game_sort'])
        review_games = review_games_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'rating': session['browse_rating']})
        pages = math.ceil(DB_REVIEWS.find(
            {
                'rating': session['browse_rating']
                }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'rating': session['browse_rating']
                }).count()
        review_ratings = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with name chosen in browse form
    elif session['game_name']:
        # initialization for all variables required for rendering results
        review_latest_sort = DB_REVIEWS.find(
            {
                'game_name': session['game_name']
                }).sort(
                    'review_id', session['review_sort'])
        review_latest = review_latest_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_users_sort = DB_REVIEWS.find(
            {
                'game_name': session['game_name']
                }).sort(
                    'username', session['user_sort'])
        review_users = review_users_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_ratings_sort = DB_REVIEWS.find(
            {
                'game_name': session['game_name']
                }).sort(
                    'rating', session['rating_sort'])
        review_ratings = review_ratings_sort.skip(
            session['SKIP']).limit(session['LIMIT'])
        review_not_sorted = DB_REVIEWS.find(
            {
                'game_name': session['game_name']})
        pages = math.ceil(DB_REVIEWS.find(
            {
                'game_name': session['game_name']
                }).count()/session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'game_name': session['game_name']
                }).count()
        review_games = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        all_reviews = review_not_sorted.skip(
            session['SKIP']).limit(session['LIMIT'])
        return render_template(
                                'browse.html',
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render template with nothing chosen in browse form requires
    # initial initialization of variables in the start of function
    else:
        return render_template(
                                'browse.html',
                                not_selected=True,
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                results=results,
                                users=users,
                                games=games,
                                pages=pages,
                                PAGE_NUMBER=session['PAGE_NUMBER'])


# rendering template for your reviews
@app.route('/your_reviews', methods=['POST', 'GET'])
def your_reviews():
    # checks if there is a user in session or else redirects to fail login
    if 'username' in session:
        # initialization for all variables required for rendering results
        ureviews = DB_REVIEWS.find(
            {
                'username': session['username']
                }).skip(session['SKIP']).limit(session['LIMIT'])
        results = DB_REVIEWS.find(
            {
                'username': session['username']
                }).count()
        pages = math.ceil(DB_REVIEWS.find(
            {
                'username': session['username']
                }).count()/session['LIMIT'])
        games = DB_GAME_LIST.find().sort('name', 1)
        # sets variables for search query and redirects back to your_reviews()
        if request.method == 'POST':
            game_json = request.form['game_select']
            browse_rating = request.form['browse_rating']
            if game_json != "":
                game_objects = game_json.split(',')
                game_name_slice_front = game_objects[1][10:]
                game_name = game_name_slice_front[:-1]
                game = DB_GAME_LIST.find_one({'name': game_name})
                session['game_name'] = game['name']
                session['game_picture'] = game['picture_link']
                session['game_wiki_link'] = game['wiki_link']
                session['game_description'] = game['game_description']
            if browse_rating != "":
                session['browse_rating'] = int(request.form['browse_rating'])
            return redirect(url_for('your_reviews'))
        # render template with game and rating chosen in your_reviews form
        if session['game_name'] and session['browse_rating']:
                # initialization for all variables
                # required for rendering results
                ureviews = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating'],
                        'game_name': session['game_name']
                        }).skip(session['SKIP']).limit(session['LIMIT'])
                pages = math.ceil(DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating'],
                        'game_name': session['game_name']
                        }).count()/session['LIMIT'])
                result = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating'],
                        'game_name': session['game_name']
                        }).count()
                return render_template(
                                        'your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])
        # render template with game chosen in your_reviews form
        elif session['game_name']:
                # initialization for all variables
                # required for rendering results
                ureviews = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'game_name': session['game_name']
                        }).skip(session['SKIP']).limit(session['LIMIT'])
                pages = math.ceil(DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'game_name': session['game_name']
                        }).count()/session['LIMIT'])
                result = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'game_name': session['game_name']
                        }).count()
                return render_template(
                                        'your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])
        # render template with rating chosen in your_reviews form
        elif session['browse_rating']:
                # initialization for all variables
                # required for rendering results
                ureviews = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating']
                        }).skip(session['SKIP']).limit(session['LIMIT'])
                pages = math.ceil(DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating']
                        }).count()/session['LIMIT'])
                result = DB_REVIEWS.find(
                    {
                        'username': session['username'],
                        'rating': session['browse_rating']
                        }).count()
                return render_template(
                                        'your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])
        # render template with nothing chosen in your_reviews form
        return render_template(
                                'your_reviews.html',
                                ureviews=ureviews,
                                games=games,
                                results=results,
                                pages=pages,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    # render no_login template when no username in session
    return render_template('no_login.html')


# rendering template for top_games
@app.route('/top_games')
def top_games():
    # initialization for all variables required for
    # upating the game keys required to show and update results
    total_ratings = DB_REVIEWS.aggregate(
        [
            {
                '$group': {
                    '_id': '$game_name',
                    'count': {
                        '$sum': '$rating'}}}])
    total_reviews = DB_REVIEWS.aggregate(
        [
            {
                '$group': {
                    '_id': '$game_name',
                    'count': {
                        '$sum': 1}}}])
    grp_average = DB_GAME_LIST.aggregate(
        [
            {
                '$group': {
                    '_id': '$name',
                    'avgAmount': {
                        '$avg': {
                            '$divide': ['$total_rating',
                                        '$total_reviews']}}}}])
    # updating game keys in order to show
    # correct averages, ratings and total ratings
    for rating in total_ratings:
        DB_GAME_LIST.update(
            {
                'name': rating['_id']
                }, {
                    '$set': {
                        'total_rating': rating['count']}})
    for review in total_reviews:
        DB_GAME_LIST.update(
            {
                'name': review['_id']
                }, {
                    '$set': {
                        'total_reviews': review['count']}})
    for grp in grp_average:
        if grp['avgAmount'] is None:
            continue
        average = round(grp['avgAmount'], 2)
        DB_GAME_LIST.update(
            {
                'name': grp['_id']
                }, {
                    '$set': {'average': average}})
    # sort by average, rating and total rating
    # in order to show results correctly on template
    best_avg = DB_GAME_LIST.find().sort('average', -1).limit(6)
    most_reviews = DB_GAME_LIST.find().sort('total_reviews', -1).limit(6)
    most_rating = DB_GAME_LIST.find().sort('total_rating', -1).limit(6)
    return render_template(
                            'top_games.html',
                            best_avg=best_avg,
                            most_reviews=most_reviews,
                            most_rating=most_rating)


# rendering templates for admin sites,
# check if admin is logged in before rendering results
@app.route('/admin_tab_games')
def admin_tab_games():
    if session['admin']:
        gamelist = DB_GAME_LIST.find().skip(
            session['SKIP']).limit(session['LIMIT'])
        pages = math.ceil(DB_GAME_LIST.find().count()/session['LIMIT'])
        results = DB_GAME_LIST.find().count()
        return render_template(
                                'admin_tab_games.html',
                                gamelist=gamelist,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    return render_template('no_login.html')


@app.route('/admin_tab_users')
def admin_tab_users():
    if session['admin']:
        users = DB_USERS.find().skip(session['SKIP']).limit(session['LIMIT'])
        pages = math.ceil(DB_USERS.find().count()/session['LIMIT'])
        results = DB_USERS.find().count()
        return render_template(
                                'admin_tab_users.html',
                                users=users,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    return render_template('no_login.html')


@app.route('/admin_tab_suggestions')
def admin_tab_suggestions():
    if session['admin']:
        suggestions = DB_GAME_SUGGESTION.find().skip(
            session['SKIP']).limit(session['LIMIT'])
        pages = math.ceil(DB_GAME_SUGGESTION.find().count()/session['LIMIT'])
        results = DB_GAME_SUGGESTION.find().count()
        return render_template(
                                'admin_tab_suggestions.html',
                                suggestions=suggestions,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    return render_template('no_login.html')


@app.route('/admin_tab_reviews')
def admin_tab_reviews():
    if session['admin']:
        reviews = DB_REVIEWS.find().sort(
            'review_id', 1).skip(
                session['SKIP']).limit(session['LIMIT'])
        pages = math.ceil(DB_REVIEWS.find().count()/session['LIMIT'])
        results = DB_REVIEWS.find().count()
        return render_template(
                                'admin_tab_reviews.html',
                                reviews=reviews,
                                pages=pages,
                                results=results,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
    return render_template('no_login.html')
