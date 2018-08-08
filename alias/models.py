from alias import db
from flask_login import UserMixin
from alias import login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_teacher = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Translems(db.Model):
    __tablename__ = 'translems'
    id = db.Column(db.Integer, primary_key=True)
    russian = db.Column(db.String(64), index=True, nullable=False)
    english = db.Column(db.String(64), index=True, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('russian', 'english', 'topic_id', name='_my_constrain'), )

    def __repr__(self):
        return f'<Table> {self.__tablename__}'

    @staticmethod
    def get_ids_by_topic_id(topic_id):
        ids = Translems.query.filter(Translems.topic_id == topic_id).values(Translems.id)
        return [translem_id for (translem_id,) in ids]

    @staticmethod
    def get_russian(translem_id):
        russian = Translems.query.filter(Translems.id == translem_id).value(Translems.russian)
        return russian

    @staticmethod
    def get_english(translem_id):
        english = Translems.query.filter(Translems.id == translem_id).value(Translems.english)
        return english


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(64), unique=True)
    translems = db.relationship('Translems', backref='topic', cascade='all, delete, delete-orphan',
                                single_parent='True')

    def __repr__(self):
        return f'<Table> {self.__tablename__}'

    @staticmethod
    def get_id_by_name(name):
        return Topic.query.filter(Topic.topic_name == name).first().id


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
