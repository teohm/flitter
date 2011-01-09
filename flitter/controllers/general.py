from flask import Module, render_template, request, g, flash, session, \
                  redirect, url_for, current_app

mod = Module(__name__)


@mod.route('/')
def index():
    return render_template('index.html')
    
