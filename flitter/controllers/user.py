from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, abort, current_app
from ..services import UserService, SecureHashService

mod = Module(__name__)


@mod.before_app_request
def before_app_request():
    g.userservice = UserService(g.db, SecureHashService(
        current_app.config['SECRET_KEY'], 'sha256'))


@mod.route('/welcome', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not g.userservice.user_exists(username):
            g.userservice.signup(username, password)
            session['user'] = username
            flash('Welcome, {}.'.format(username))
            return redirect(url_for('entry.entries', username=username))
        else:
            error = 'Username already in used'
        
    return render_template('signup.html', error=error)


@mod.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful')
    return redirect(url_for('general.index'))
    
    
@mod.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if g.userservice.check_credential(username, password):
            session['user'] = username
            return redirect(url_for('entry.entries', username=username))
        else:
            error = 'Invalid username or password'
    
    return render_template('login.html', error=error)
    