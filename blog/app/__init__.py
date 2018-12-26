from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_bootstrap import Bootstrap
from flask_jwt import JWT
from flask import g
from config import config

db = SQLAlchemy()
redis_store = FlaskRedis()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    redis_store.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    db.app = app
    from app.controller.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    @app.before_request
    def before_request():
        g.authorization = request.headers.get('Authorization')
        # g.current_url = request.headers.get('')



    from app.controller.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    from app.controller.admin.user import user as admin_user_blueprint
    app.register_blueprint(admin_user_blueprint, url_prefix="/admin/user")
    from app.controller.common import common as common_blueprint
    app.register_blueprint(common_blueprint)

    return app
