import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'isdjfoadfnaogi84903gldjg9eu0gljs9e3jpj3p9gldjgo93u04telkkflgjoeut9'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://homychat:boardgames@localhost/homychat_db3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
