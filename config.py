import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_URL = 'postgresql://homychat:boardgames@localhost/homychat_db3'
    SQLALCHEMY_DATABASE_URI = os.environ.get(DATABASE_URL) or 'sqlite:///' + os.path.join(basedir, 'probe.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
