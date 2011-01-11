from flask import Flask, g, render_template, redirect, url_for
import database
import flittercfg as default_cfg

def create_app(**overwrite_cfg):
    """Builds new Flitter app.
    
    :param overwrite_cfg: settings to override `flittercfg.py`
    :return: new Flask object.
    """
    app = Flask(__name__)
    
    _load_config(app, overwrite_cfg)
    _init_db(app)
    _register_app_functions(app)
    _register_modules(app)
    
    return app


def _register_modules(app):
    base = '/flitter'
    from flitter.controllers import general, user, entry
    app.register_module(general.mod, url_prefix=base)
    app.register_module(user.mod, url_prefix=base)
    app.register_module(entry.mod, url_prefix=base)
    
    
def _register_app_functions(app):
    @app.before_request
    def before_request():
        g.db = database.connect_db(app.config['DATABASE'])
        
    @app.after_request
    def after_request(response):
        g.db.close()
        return response
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
        
    @app.route('/')
    def to_flitter():
        return redirect(url_for('general.index'))


def _load_config(app, overwrite_cfg):
    app.config.from_object(default_cfg)
    app.config.update(overwrite_cfg)

    
def _init_db(app):
    database.init_db(app.config['DATABASE'], app.config['RESET_DB'])
