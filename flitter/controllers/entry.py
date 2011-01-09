from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, abort, current_app
from ..services import EntryService, TimestampService

mod = Module(__name__)


@mod.before_request
def before_request():
    g.entryservice = EntryService(g.db, TimestampService())


@mod.route('/user/<username>', methods=['GET', 'POST'])
def entries(username):
    if not g.userservice.user_exists(username):
        current_app.logger.info(username)
        abort(404)
    
    if request.method == 'POST':
        g.entryservice.add_entry(username, request.form['content'])
        
    entries = g.entryservice.list_entries(username)
    is_owner = session.get('user', None) == username
    
    return render_template('entries.html', entries=entries,
                           username=username, is_owner=is_owner)
    