from flask import render_template, session, request, redirect, url_for
from bson.objectid import ObjectId
from app import app
from app.setup import DB_GAME_LIST, DB_USERS, DB_REVIEWS


@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    '''
    rendering template for editing a game, only available for admin
    '''
    if session['admin']:
        game = DB_GAME_LIST.find_one({"_id": ObjectId(game_id)})
        return render_template(
                                'edit_game.html',
                                game=game)
    return render_template('no_login.html')


@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    '''
    updating database according to changes made
    in edit_game template, only available for admin
    ''' 
    if session['admin']:
        DB_GAME_LIST.update(
            {
                '_id': ObjectId(game_id)
            }, {
                'name': request.form.get('name'),
                'publisher': request.form.get('publisher'),
                'picture_link': request.form.get('picture_link'),
                'wiki_link': request.form.get('wiki_link'),
                'game_description': request.form.get('game_description')
            })
        return redirect(url_for('admin_tab'))
    return render_template('no_login.html')


@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    '''
    rendering template for editing a review
    '''
    if session['username']:
        review = DB_REVIEWS.find_one({"_id": ObjectId(review_id)})
        return render_template(
                                'edit_review.html',
                                review=review,
                                gamelist=DB_GAME_LIST.find())
    return render_template('no_login.html')


@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    '''
    updating database according to changes made in edit_review
    '''
    if session['username']:
        DB_REVIEWS.update(
            {
                '_id': ObjectId(review_id)
            }, {
                'game_name': request.form.get('game_name'),
                'username': request.form.get('username'),
                'description': request.form.get('review'),
                'rating': request.form.get('rating'),
            })
        if session['admin']:
            return redirect(url_for('admin_tab'))
        return redirect(url_for('your_reviews'))
    return render_template('no_login.html')


@app.route('/edit_user/<user_id>')
def edit_user(user_id):
    '''
    rendering template for editing a user, only available for admin
    '''
    if session['admin']:
        user = DB_USERS.find_one({"_id": ObjectId(user_id)})
        return render_template(
                                'edit_user.html',
                                user=user)
    return render_template('no_login.html')


@app.route('/update_user/<user_id>/<user_name>', methods=["POST"])
def update_user(user_id, user_name):
    '''
    updating database according to changes
    made in edit_user, only available for admin
    '''
    if session['admin']:
        existing_user_name = DB_USERS.find_one({"name": user_name})
        if existing_user_name is None:
            DB_USERS.update(
                {
                    '_id': ObjectId(user_id)
                }, {
                    '$set': {
                        'name': request.form.get('name'),
                        'email': request.form.get('email')
                    }})
            return redirect(url_for('admin_tab'))
        user = DB_USERS.find_one({"_id": ObjectId(user_id)})
        return "Username already in use!" + render_template(
                                                            'edit_user.html',
                                                            user=user)
    return render_template('no_login.html')
