import bcrypt
from flask import render_template, redirect, request, url_for, request, session
from app import app
from app.setup import DB_USERS, DB_GAME_LIST, DB_REVIEWS, DB_COUNTER, admin_password, admin_user, DB_GAME_SUGGESTION
# Sign up and Login pages and authentication
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        existing_user = DB_USERS.find_one({'email': request.form['email']})
        existing_username = DB_USERS.find_one({'name': request.form['username']})
        
        if existing_user is None and existing_username is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            DB_USERS.insert({'name': request.form['username'], 'password': hashpass, 'email': request.form['email']})
            session['username'] = request.form['username']
            DB_COUNTER.update({'counter_name': 'counter'}, { '$inc': {'number_users': 1}})
            if (session['username'] == admin_user) and (request.form['password'] == admin_password):
                session['admin'] = True
                return redirect(url_for('admin_tab'))
            else:
                session['admin'] = False
            return redirect(url_for('index'))
        return render_template('fail_sign_up.html')
    return render_template('sign_up.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_user = DB_USERS.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = login_user['name']
                if (session['username'] == admin_user) and (request.form['password'] == admin_password):
                    session['admin'] = True
                    return redirect(url_for('admin_tab'))
                else:
                    session['admin'] = False
                return redirect(url_for('index'))
        return render_template('fail_login.html')
    return render_template('login.html')
# clear all sessions and therefor be logged out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# root/admin access and home page for admin
@app.route('/admin_tab')
def admin_tab():
    if session['admin']:
        return render_template('admin_tab.html')
    return render_template('no_login.html')