import bcrypt
from flask import render_template, redirect, request, url_for, request, session
from app import app
from app.setup import (
                        DB_USERS,
                        DB_GAME_LIST,
                        DB_REVIEWS,
                        DB_COUNTER,
                        DB_GAME_SUGGESTION)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    '''
    Sign up and Login pages and authentication
    '''
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
            session['username'] = request.form['username']
            DB_COUNTER.update(
                {
                    'counter_name': 'counter'
                    }, {
                        '$inc': {
                            'number_users': 1
                            }})
            session['admin'] = False
            return redirect(url_for('index'))
        return render_template('fail_sign_up.html')
    return render_template('sign_up.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_user = DB_USERS.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf8'), login_user['password']):
                session['username'] = login_user['name']
                if login_user['admin'] == True:
                    session['admin'] = True
                    return redirect(url_for('admin_tab'))
                else:
                    session['admin'] = False
                return redirect(url_for('index'))
        return render_template('fail_login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    '''
    clear all sessions and therefor be logged out
    '''
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin_tab')
def admin_tab():
    '''
    root/admin access and home page for admin
    '''
    if session['admin']:
        return render_template('admin_tab.html')
    return render_template('no_login.html')
