from flask import render_template, redirect, session, request, url_for

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_COUNTER, DB_GAME_SUGGESTION
# adding a review
@app.route('/add_review')
def add_review():
    if 'username' in session:
        return render_template('add_review.html',
                                gamelist=DB_GAME_LIST.find())
    return render_template('no_login.html')

@app.route('/insert_review', methods=['POST'])
def insert_review():
    count_reviews = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count=int(count_reviews['number_reviews']+1)
    DB_REVIEWS.insert({'review_id': new_count, 'game_name': request.form['game_name'], 'username': session['username'], 'description': request.form['review'], 'rating': int(request.form['rating'])})
    DB_COUNTER.update({'counter_name': 'counter'}, { '$inc': {'number_reviews': 1}})
    if session['admin']:
        return redirect(url_for('admin_tab'))
    return redirect(url_for('your_reviews', insert_review=True))

# adding a game
@app.route('/add_game')
def add_game():
    if 'username' in session:
        return render_template('add_game.html')
    return render_template('no_login.html')

@app.route('/insert_game', methods=['POST'])
def insert_game():
    count_games = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count=int(count_games['number_games']+1)
    DB_GAME_LIST.insert({'game_id': int(new_count+1), 'name': request.form['name'], 'publisher': request.form['publisher'], 'picture_link': request.form['picture_link'], 'wiki_link': request.form['wiki_link'], 'average': 0})
    DB_COUNTER.update({'counter_name': 'counter'}, { '$inc': {'number_games': 1}})
    return redirect(url_for('admin_tab'))

@app.route('/suggest_game')
def suggest_game():
    if 'username' in session:
        return render_template('suggest_game.html')
    return render_template('no_login.html')

@app.route('/insert_suggest_game', methods=['POST'])
def insert_suggest_game():
    count_suggestions = DB_COUNTER.find_one({'counter_name': 'counter'})
    new_count=int(count_suggestions['number_suggestions']+1)
    DB_GAME_SUGGESTION.insert({'suggestion_id': int(new_count+1), 'name': request.form['name'], 'publisher': request.form['publisher'], 'picture_link': request.form['picture_link'], 'wiki_link': request.form['wiki_link']})
    DB_COUNTER.update({'counter_name': 'counter'}, { '$inc': {'number_suggestions': 1}})
    
    return redirect(url_for('your_reviews', insert_game=True))


