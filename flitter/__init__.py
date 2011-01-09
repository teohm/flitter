from flask import Flask, g
import database
import flittercfg as default_cfg

def create_app(**overwrite_cfg):
    app = Flask(__name__)
    
    _load_config(app, overwrite_cfg)
    _init_db(app)
    _register_app_functions(app)
    _register_modules(app)
    
    return app


def _register_modules(app):
    from flitter.controllers import general, user, entry
    app.register_module(general.mod)
    app.register_module(user.mod)
    app.register_module(entry.mod)
    
    
def _register_app_functions(app):
    @app.before_request
    def before_request():
        g.db = database.connect_db(app.config['DATABASE'])
        
    @app.after_request
    def after_request(response):
        g.db.close()
        return response


def _load_config(app, overwrite_cfg):
    app.config.from_object(default_cfg)
    app.config.update(overwrite_cfg)

    
def _init_db(app):
    database.init_db(app.config['DATABASE'], app.config['RESET_DB'])
