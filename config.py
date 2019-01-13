import os

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty98@localhost/newdata'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'SuperMegaSecretKey'

