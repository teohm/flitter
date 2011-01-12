from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, abort, current_app
from ..services import UserService, SecureHashService

mod = Module(__name__)

@mod.before_app_request
def before_app_request():
    g.userservice = UserService(g.db, SecureHashService(
                                        current_app.config['SECRET_KEY']))

@mod.route('/welcome', methods=['GET', 'POST'])
def signup():
    if is_authenticated():
        return redirect_to_user_page()
        
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
    if is_authenticated():
        return redirect_to_user_page()
        
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
    


def is_authenticated():
    """Returns true if user session is autheticated, otherwise False."""
    return session.has_key('user')
    
def redirect_to_user_page():
    """Redirects to user entry page.
    
    It expects user session is authenticated, and
    session['user'] contains username.
    """
    return redirect(url_for('entry.entries', username=session['user']))