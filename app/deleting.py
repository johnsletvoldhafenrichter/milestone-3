from flask import render_template, session, request, redirect, url_for
from bson.objectid import ObjectId
from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS, DB_GAME_SUGGESTION


# admin only deleting a game from database
@app.route('/delete_game/<game_id>/<game_name>')
def delete_game(game_id, game_name):
    if session['admin']:
        DB_REVIEWS.remove({'game_name': game_name})
        DB_GAME_LIST.remove({'_id': ObjectId(game_id)})
        return redirect(url_for('admin_tab_games'))
    return render_template('no_login.html')


# admin only deleting a user from database
@app.route('/delete_user/<user_id>/<review_name>')
def delete_user(user_id, review_name):
    if session['admin']:
        DB_REVIEWS.remove({'username': review_name})
        DB_USERS.remove({'_id': ObjectId(user_id)})
        return redirect(url_for('admin_tab_users'))
    return render_template('no_login.html')


# deleting a review that you created, or admin can delete all reviews
@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    if session['username']:
        DB_REVIEWS.remove({'_id': ObjectId(review_id)})
        if session['admin']:
            return redirect(url_for('admin_tab_reviews'))
        return redirect(url_for('your_reviews'))
    return render_template('no_login.html')


# resetting the sorting and and choices made in browsing
@app.route('/clear_sessions/<where>')
def clear_sessions(where):
    session['browse_user'] = False
    session['browse_rating'] = False
    session['game_name'] = False
    session['SKIP'] = 0
    session['PAGE_NUMBER'] = 1
    session['LIMIT'] = int(6)
    return redirect(url_for(where))


# admin only deleting suggestions
@app.route('/delete_suggested_game/<game_id>/<game_name>')
def delete_suggested_game(game_id, game_name):
    if session['admin']:
        DB_GAME_SUGGESTION.remove({'_id': ObjectId(game_id)})
        return redirect(url_for('admin_tab_suggestions'))
    return render_template('no_login.html')
