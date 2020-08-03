from flask import render_template, session, request, redirect, url_for
from bson.objectid import ObjectId

from app import app
from app.setup import DB_GAME_LIST, DB_REVIEWS, DB_USERS

@app.route('/delete_game/<game_id>/<game_name>')
def delete_game(game_id, game_name):
    if session['admin']:
        DB_REVIEWS.remove({'game_name': game_name})
        DB_GAME_LIST.remove({'_id': ObjectId(game_id)})
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')

@app.route('/delete_user/<user_id>/<review_name>')
def delete_user(user_id, review_name):
    if session['admin']:
        DB_REVIEWS.remove({'username': review_name})
        DB_USERS.remove({'_id': ObjectId(user_id)})
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    if session['username']:
        DB_REVIEWS.remove({'_id': ObjectId(review_id)})
        if session['admin']:
            return redirect(url_for('admin_tab'))
        return redirect(url_for('your_reviews'))
    return render_template('no_login.html')