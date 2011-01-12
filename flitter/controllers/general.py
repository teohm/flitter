from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, current_app
from .user import is_authenticated, redirect_to_user_page
mod = Module(__name__)

@mod.route('/')
def index():
    if is_authenticated():
        return redirect_to_user_page()
        
    return render_template('index.html')

    