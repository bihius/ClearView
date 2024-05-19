from flask import Flask, Blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'swTsOpveqmquuai11jope0fnv04dj7I9zuthx18tjuglrt4ut9fus2hzxn2lu4i6' #dont know where to put this

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app