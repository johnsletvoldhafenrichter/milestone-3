from flask import render_template, session, request, redirect, url_for
from flask_pymongo import PyMongo, pymongo, DESCENDING
import math

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS, DB_COUNTER

@app.route('/')
def index():
    session['LIMIT'] = int(6)
    session['TOTAL_PAGES'] = math.ceil(DB_REVIEWS.find().count()/session['LIMIT'])
    session['SKIP'] = 0
    session['PAGE_NUMBER'] = 1
    # sorting initialization
    session['user_sort']=False
    session['rating_sort']=False
    session['game_sort']=False
    session['review_sort']=False
    
    session['browse_user']=False
    session['browse_rating']=False
    session['game_name']=False
    
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

@app.route('/page_count/<num>/<where>')
def page_count(num, where):
    if where == 'browse':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(DB_REVIEWS.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for('browse') + '#sorting')
    elif where == 'all_games':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(DB_GAME_LIST.find().count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for('all_games'))
    elif where == 'your_reviews':
        session['PAGE_NUMBER'] = int(num)
        session['TOTAL_PAGES'] = math.ceil(DB_REVIEWS.find({'username': session['username']}).count()/session['LIMIT'])
        if session['PAGE_NUMBER'] < 1:
            session['PAGE_NUMBER'] = 1
            session['SKIP'] = 0
        elif session['PAGE_NUMBER'] > session['TOTAL_PAGES']:
            session['PAGE_NUMBER'] = session['TOTAL_PAGES']
        session['SKIP'] = int((session['PAGE_NUMBER']-1)*session['LIMIT'])
        return redirect(url_for('your_reviews') + '#search')

@app.route('/change_limit/<num>/<where>')
def change_limit(num, where):
    if where:
        session['LIMIT'] = int(num)
        return redirect(url_for('page_count', num=1, where=where))
    else:
        return redirect(url_for('404.html'))

@app.route('/all_games')
def all_games():
    gamelist=DB_GAME_LIST.find().skip(session['SKIP']).limit(session['LIMIT'])
    results=DB_GAME_LIST.find().count()
    pages=math.ceil(DB_GAME_LIST.find().count()/session['LIMIT'])
    return render_template('all_games.html',
                            gamelist=gamelist,
                            pages=pages,
                            results=results,
                            PAGE_NUMBER=session['PAGE_NUMBER'])

@app.route('/sorting/<el>')
def sorting(el):
    if el == 'user':
        if session['user_sort'] == 1:
            session['user_sort']=-1
            session['rating_sort']=False
            session['game_sort']=False
            session['review_sort']=False
        else:
            session['user_sort']=1
            session['rating_sort']=False
            session['game_sort']=False
            session['review_sort']=False
    elif el == 'rating':
        if session['rating_sort'] == 1:
            session['rating_sort']=-1
            session['user_sort']=False
            session['game_sort']=False
            session['review_sort']=False
        else:
            session['rating_sort']=1
            session['user_sort']=False
            session['game_sort']=False
            session['review_sort']=False
    elif el == 'game':
        if session['game_sort'] == 1:
            session['game_sort']=-1
            session['rating_sort']=False
            session['user_sort']=False
            session['review_sort']=False
        else:
            session['game_sort']=1
            session['rating_sort']=False
            session['user_sort']=False
            session['review_sort']=False
    elif el == 'latest':
        if session['review_sort'] == 1:
            session['review_sort']=-1
            session['rating_sort']=False
            session['game_sort']=False
            session['user_sort']=False
        else:
            session['review_sort']=1
            session['rating_sort']=False
            session['game_sort']=False
            session['user_sort']=False
    return redirect(url_for('browse') + '#sorting')

@app.route('/browse', methods=['POST', 'GET'])
def browse():
    review_ratings_sort=DB_REVIEWS.find().sort('rating', session['rating_sort'])
    review_users_sort=DB_REVIEWS.find().sort('username', session['user_sort'])
    review_games_sort=DB_REVIEWS.find().sort('game_name', session['game_sort'])
    review_latest_sort=DB_REVIEWS.find().sort('review_id', session['review_sort'])

    all_reviews = DB_REVIEWS.find().skip(session['SKIP']).limit(session['LIMIT'])

    review_ratings=review_ratings_sort.skip(session['SKIP']).limit(session['LIMIT'])
    review_users=review_users_sort.skip(session['SKIP']).limit(session['LIMIT'])
    review_games=review_games_sort.skip(session['SKIP']).limit(session['LIMIT'])
    review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])

    users = DB_USERS.find().sort('name', 1)
    games = DB_GAME_LIST.find().sort('name', 1)

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
        return redirect(url_for('browse'))

    if session['browse_user'] and session['game_name'] and session['browse_rating']:
        review_latest_sort=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name'], 'rating': session['browse_rating']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])
        
        review_not_sorted=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name'], 'rating': session['browse_rating']})
        pages=math.ceil(DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name'], 'rating': session['browse_rating']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name'], 'rating': session['browse_rating']}).count()

        review_users=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        review_ratings=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        review_games=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
    
        return render_template('browse.html',
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
    elif session['browse_user'] and session['browse_rating']:
        review_latest_sort=DB_REVIEWS.find({'username': session['browse_user'], 'rating': session['browse_rating']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])
        
        review_games_sort=DB_REVIEWS.find({'username': session['browse_user'], 'rating': session['browse_rating']}).sort('game_name', session['game_sort'])
        review_games=review_games_sort.skip(session['SKIP']).limit(session['LIMIT'])
        
        review_not_sorted=DB_REVIEWS.find({'username': session['browse_user'], 'rating': session['browse_rating']})
        pages=math.ceil(DB_REVIEWS.find({'username': session['browse_user'], 'rating': session['browse_rating']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'username': session['browse_user'], 'rating': session['browse_rating']}).count()

        review_users=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        review_games=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        
        return render_template('browse.html',
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
    elif session['browse_user'] and session['game_name']:
        review_latest_sort=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])
        
        review_ratings_sort=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name']}).sort('rating', session['rating_sort'])
        review_ratings=review_ratings_sort.skip(session['SKIP']).limit(session['LIMIT'])
        
        review_not_sorted=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name']})
        pages=math.ceil(DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'username': session['browse_user'], 'game_name': session['game_name']}).count()

        review_users=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        review_games=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        
        return render_template('browse.html',
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
    elif session['browse_rating'] and session['game_name']:
        review_latest_sort=DB_REVIEWS.find({'rating': session['browse_rating'], 'game_name': session['game_name']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_users_sort=DB_REVIEWS.find({'rating': session['browse_rating'], 'game_name': session['game_name']}).sort('username', session['user_sort'])
        review_users=review_users_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_not_sorted=DB_REVIEWS.find({'rating': session['browse_rating'], 'game_name': session['game_name']})
        pages=math.ceil(DB_REVIEWS.find({'rating': session['browse_rating'], 'game_name': session['game_name']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'rating': session['browse_rating'], 'game_name': session['game_name']}).count()

        review_ratings=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        review_games=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])

        return render_template('browse.html',
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
    elif session['browse_user']:
        review_latest_sort=DB_REVIEWS.find({'username': session['browse_user']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_ratings_sort=DB_REVIEWS.find({'username': session['browse_user']}).sort('rating', session['rating_sort'])
        review_ratings=review_ratings_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_games_sort=DB_REVIEWS.find({'username': session['browse_user']}).sort('game_name', session['game_sort'])
        review_games=review_games_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_not_sorted=DB_REVIEWS.find({'username': session['browse_user']})
        pages=math.ceil(DB_REVIEWS.find({'username': session['browse_user']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'username': session['browse_user']}).count()

        review_users=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])

        return render_template('browse.html',
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
    elif session['browse_rating']:
        review_latest_sort=DB_REVIEWS.find({'rating': session['browse_rating']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_users_sort=DB_REVIEWS.find({'rating': session['browse_rating']}).sort('username', session['user_sort'])
        review_users=review_users_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_games_sort=DB_REVIEWS.find({'rating': session['browse_rating']}).sort('game_name', session['game_sort'])
        review_games=review_games_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_not_sorted=DB_REVIEWS.find({'rating': session['browse_rating']})
        pages=math.ceil(DB_REVIEWS.find({'rating': session['browse_rating']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'rating': session['browse_rating']}).count()

        review_ratings=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])

        return render_template('browse.html',
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
    elif session['game_name']:
        review_latest_sort=DB_REVIEWS.find({'game_name': session['game_name']}).sort('review_id', session['review_sort'])
        review_latest=review_latest_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_users_sort=DB_REVIEWS.find({'game_name': session['game_name']}).sort('username', session['user_sort'])
        review_users=review_users_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_ratings_sort=DB_REVIEWS.find({'game_name': session['game_name']}).sort('rating', session['rating_sort'])
        review_ratings=review_ratings_sort.skip(session['SKIP']).limit(session['LIMIT'])

        review_not_sorted=DB_REVIEWS.find({'game_name': session['game_name']})
        pages=math.ceil(DB_REVIEWS.find({'game_name': session['game_name']}).count()/session['LIMIT'])
        results=DB_REVIEWS.find({'game_name': session['game_name']}).count()

        review_games=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])
        all_reviews=review_not_sorted.skip(session['SKIP']).limit(session['LIMIT'])

        return render_template('browse.html',
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
    else:
        return render_template('browse.html',
                                not_selected=True,
                                review_ratings=review_ratings,
                                review_users=review_users,
                                review_games=review_games,
                                review_latest=review_latest,
                                all_reviews=all_reviews,
                                users=users,
                                games=games,
                                pages=session['TOTAL_PAGES'],
                                PAGE_NUMBER=session['PAGE_NUMBER'])


@app.route('/your_reviews', methods=['POST', 'GET'])
def your_reviews():
    if 'username' in session:
        ureviews=DB_REVIEWS.find({'username': session['username']}).skip(session['SKIP']).limit(session['LIMIT'])
        results=DB_REVIEWS.find({'username': session['username']}).count()
        pages=math.ceil(DB_REVIEWS.find({'username': session['username']}).count()/session['LIMIT'])

        games=DB_GAME_LIST.find().sort('name', 1)
        if request.method == 'POST':
            game_json = request.form['game_select']
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
            if browse_rating != "":
                session['browse_rating']=int(request.form['browse_rating'])
            return redirect(url_for('your_reviews'))

        if session['game_name'] and session['browse_rating']:
                ureviews=DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating'], 'game_name': session['game_name']}).skip(session['SKIP']).limit(session['LIMIT'])
                pages=math.ceil(DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating'], 'game_name': session['game_name']}).count()/session['LIMIT'])
                result=DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating'], 'game_name': session['game_name']}).count()
                return render_template('your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])
        elif session['game_name']:
                ureviews=DB_REVIEWS.find({'username': session['username'], 'game_name': session['game_name']}).skip(session['SKIP']).limit(session['LIMIT'])
                pages=math.ceil(DB_REVIEWS.find({'username': session['username'], 'game_name': session['game_name']}).count()/session['LIMIT'])
                result=DB_REVIEWS.find({'username': session['username'], 'game_name': session['game_name']}).count()
                return render_template('your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])
        elif session['browse_rating']:
                ureviews=DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating']}).skip(session['SKIP']).limit(session['LIMIT'])
                pages=math.ceil(DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating']}).count()/session['LIMIT'])
                result=DB_REVIEWS.find({'username': session['username'], 'rating': session['browse_rating']}).count()
                return render_template('your_reviews.html',
                                        ureviews=ureviews,
                                        games=games,
                                        result=result,
                                        results=results,
                                        pages=pages,
                                        PAGE_NUMBER=session['PAGE_NUMBER'])    
        return render_template('your_reviews.html',
                                ureviews=ureviews,
                                games=games,
                                results=results,
                                pages=pages,
                                PAGE_NUMBER=session['PAGE_NUMBER'])
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
    best_avg=DB_GAME_LIST.find().sort('average', -1).limit(6)
    most_reviews=DB_GAME_LIST.find().sort('total_reviews', -1).limit(6)
    most_rating=DB_GAME_LIST.find().sort('total_rating', -1).limit(6)
        
    return render_template('top_games.html',
                            best_avg=best_avg,
                            most_reviews=most_reviews,
                            most_rating=most_rating)