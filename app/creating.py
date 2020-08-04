from flask import render_template, redirect, session, request, url_for

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS
# adding a review
@app.route('/add_review')
def add_review():
    if 'username' in session:
        return render_template('add_review.html',
                                gamelist=DB_GAME_LIST.find())
    return render_template('no_login.html')

@app.route('/insert_review', methods=['POST'])
def insert_review():
    DB_REVIEWS.insert({'game_name': request.form['game_name'], 'username': session['username'], 'description': request.form['review'], 'rating': int(request.form['rating'])})
    if session['admin']:
        return redirect(url_for('admin_tab'))
    return redirect(url_for('your_reviews'))

# adding a game
@app.route('/add_game')
def add_game():
    if 'username' in session:
        return render_template('add_game.html')
    return render_template('no_login.html')

@app.route('/insert_game', methods=['POST'])
def insert_game():
    DB_GAME_LIST.insert({'name': request.form['name'], 'publisher': request.form['publisher'], 'picture_link': request.form['picture_link'], 'wiki_link': request.form['wiki_link']})
    return redirect(url_for('admin_tab'))
