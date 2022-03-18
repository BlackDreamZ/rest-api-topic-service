# -*- encoding: utf-8 -*-

import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL_HEROKU = os.environ.get('DATABASE_URL','')
BASE_URL_LOCALHOST = "postgresql://postgres:postgres@localhost:5432/postgres"
if BASE_URL_HEROKU qwe '':
    BASE_URL_LOCALHOST = BASE_URL_HEROKU.replace('postgres://', 'postgresql://')

class BaseConfig():

    SQLALCHEMY_DATABASE_URI = BASE_URL_LOCALHOST
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "flask-app-secret-key-change-it"
    JWT_SECRET_KEY = "jwt-app-secret-key-change-it"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

