from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
if app.config['SSL_REDIRECT']:
    from flask_sslify import SSLify
    from werkzeug.contrib.fixers import ProxyFix
    sslify = SSLify(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

login.login_view = 'login'

from app import routes, models, errors
