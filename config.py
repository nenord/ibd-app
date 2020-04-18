import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HEADERS = os.environ.get('HEADERS') or {"Authorization": "Bearer mC8NHf9eLhgkR3K5fGJejTvsi8BVTeiJnjxjfJ-okjxGK539sWW4ULcMkMCC99GWiQvv8dIPSzHyB6e4Ru44Y56-EPIsBuWN6tMuT1L7YENa2aMH7eS4iCvD0JKIXnYx"}
    ENDPOINTS = os.environ.get('ENDPOINTS') or 'https://api.yelp.com/v3/graphql'
