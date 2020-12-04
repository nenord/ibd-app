import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HEADERS = os.environ.get('HEADERS')
    ENDPOINTS = os.environ.get('ENDPOINTS') or 'https://api.yelp.com/v3/graphql'
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
