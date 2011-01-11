from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, abort, current_app
from ..services import EntryService, TimestampService

mod = Module(__name__)

@mod.before_request
def before_request():
    g.entryservice = EntryService(g.db, TimestampService())

@mod.route('/user/<username>', methods=['POST'])
def add_entry(username):
    ensure_user_exists(username)
    entry = g.entryservice.add_entry(username, request.form['content'])
    return render_template('entrylist.html', entries=[entry], is_ajax=True)
        
@mod.route('/user/<username>', methods=['GET'])
def entries(username):
    limit = current_app.config['ENTRIES_PER_PAGE']
    ensure_user_exists(username)
    return show_entries(username,
                        request.args.get('limit', limit, type=int),
                        request.args.get('offset', 0, type=int),
                        request.args.get('is_ajax', False, type=bool))


def ensure_user_exists(username):
    if not g.userservice.user_exists(username): abort(404)

def show_entries(username, limit, offset, is_ajax):
    entries = g.entryservice.list_entries(username, limit, offset)
    return render_template('entrylist.html',
        entries = entries,
        username = username,
        is_ajax = is_ajax,
        next_link = gen_next_link(username, entries, limit, offset),
        is_owner = session.get('user', None) == username,
        max_length = current_app.config['ENTRY_MAX_LENGTH']      
    )

def gen_next_link(username, entries, limit, current_offset):
    is_last_page = len(entries) < limit
    if is_last_page: return None
    
    next_offset = current_offset + limit
    return url_for('entries', username=username,
                              limit=limit,
                              offset=next_offset,
                              is_ajax=True)
