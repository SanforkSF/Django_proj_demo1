import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/interflaska'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "key_key"
    DEBUG = True