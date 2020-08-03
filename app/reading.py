from flask import render_template, session, request, redirect, url_for

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
        game_objects = game_json.split(',')
        game_name_slice_front = game_objects[1][10:]
        game_name = game_name_slice_front[:-1]
        game_pic_slice_front = game_objects[3][18:]
        game_pic = game_pic_slice_front[:-1]
        wiki_link_slice_front = game_objects[4][15:]
        wiki_link = wiki_link_slice_front[:-1]
        
        return render_template('browse.html',
                                reviews=DB_REVIEWS.find( {'$query': {}, '$orderby': { 'username' : 1 } } ),
                                games=DB_GAME_LIST.find(),
                                name=game_name,
                                picture=game_pic,
                                wiki_link=wiki_link,
                                users=DB_USERS.find({'$query': {}, '$orderby': { 'name' : 1 } } ))
    return render_template('browse.html',
                            reviews=DB_REVIEWS.find(),
                            games=DB_GAME_LIST.find())

@app.route('/your_reviews')
def your_reviews():
    if 'username' in session:
        return render_template('your_reviews.html',
                                ureviews=DB_REVIEWS.find({'username': session['username']}),
                                game_list=DB_GAME_LIST.find())
    return render_template('no_login.html')