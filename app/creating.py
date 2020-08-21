from flask import render_template, redirect, session, request, url_for
import bcrypt
from bson.objectid import ObjectId
from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_COUNTER, DB_GAME_SUGGESTION, DB_USERS


@app.route('/add_review')
def add_review():
    '''
    rendering template for adding a review
    '''
    if 'username' in session:
        return render_template(
                                'add_review.html',
                                gamelist=DB_GAME_LIST.find().sort('name', 1))
    return render_template('no_login.html')


@app.route('/insert_review', methods=['POST'])
def insert_review():
    '''
    inserting review into database
    '''
    count_reviews = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count = int(count_reviews['number_reviews']+1)
    DB_REVIEWS.insert(
        {
            'review_id': new_count,
            'game_name': request.form['game_name'],
            'username': session['username'],
            'description': request.form['review'],
            'rating': int(request.form['rating'])
        })
    DB_COUNTER.update(
        {
            'counter_name': 'counter'
        }, {
            '$inc': {
                    'number_reviews': 1
                    }
        })

    if session['admin']:
        return redirect(url_for('admin_tab_reviews'))
    return redirect(url_for('your_reviews'))


@app.route('/add_game')
def add_game():
    '''
    rendering template for adding a game
    '''
    if 'username' in session:
        return render_template('add_game.html')
    return render_template('no_login.html')


@app.route('/insert_game', methods=['POST'])
def insert_game():
    '''
    inserting a game into database
    '''
    count_games = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count = int(count_games['number_games']+1)
    DB_GAME_LIST.insert(
        {
            'name': request.form['name'],
            'publisher': request.form['publisher'],
            'picture_link': request.form['picture_link'],
            'wiki_link': request.form['wiki_link'],
            'game_description': request.form['game_description'],
            'game_id': int(new_count+1),
            'average': 0
            })
    DB_COUNTER.update(
        {
            'counter_name': 'counter'
            }, {
                '$inc': {
                    'number_games': 1
                    }})
    DB_GAME_SUGGESTION.remove({'name': request.form['name']})
    return redirect(url_for('admin_tab_games'))


@app.route('/suggest_game')
def suggest_game():
    '''
    rendering template for suggesting a game
    '''
    if 'username' in session:
        return render_template('suggest_game.html')
    return render_template('no_login.html')


@app.route('/insert_suggest_game', methods=['POST'])
def insert_suggest_game():
    '''
    inserting a suggestion into the database
    '''
    count_suggestions = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count = int(count_suggestions['number_suggestions']+1)
    DB_GAME_SUGGESTION.insert(
        {
            'suggestion_id': int(new_count+1),
            'name': request.form['name'],
            'publisher': request.form['publisher'],
            'picture_link': request.form['picture_link'],
            'wiki_link': request.form['wiki_link']
            })
    DB_COUNTER.update(
        {
            'counter_name': 'counter'
            }, {
                '$inc': {
                    'number_suggestions': 1
                    }})
    return redirect(url_for('your_reviews'))


@app.route('/add_suggest_game/<game_id>')
def add_suggest_game(game_id):
    '''
    inserting a suggestion into the game_list database, for admin only
    '''
    if 'admin' in session:
        game = DB_GAME_SUGGESTION.find_one({"_id": ObjectId(game_id)})
        return render_template(
                                'add_suggest_game.html',
                                game=game)
    return render_template('no_login.html')

@app.route('/insert_user', methods=['POST'])
def insert_user():
    '''
    inserting a user, only available for admin
    '''
    if 'admin' in session:
        if request.method == 'POST':
            existing_user = DB_USERS.find_one({'email': request.form['email']})
            existing_username = DB_USERS.find_one(
                {
                    'name': request.form['username']
                    })
            if existing_user is None and existing_username is None:
                hashpass = bcrypt.hashpw(
                    request.form['password'].encode('utf-8'),
                    bcrypt.gensalt())
                DB_USERS.insert(
                    {
                        'name': request.form['username'],
                        'password': hashpass,
                        'email': request.form['email'],
                        'admin': False
                        })
                DB_COUNTER.update(
                    {
                        'counter_name': 'counter'
                        }, {
                            '$inc': {
                                'number_users': 1
                                }})
                return redirect(url_for('admin_tab_users'))
            return render_template('fail_sign_up.html')
        return render_template('sign_up.html')
