import random

from flask import render_template, flash, redirect, url_for, request, jsonify
from alias import app, db
from alias.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from alias.models import User, Topic, Translems
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
# @login_required
def index():
    topics = get_topics()
    return render_template('index.html', topics=topics)


def get_topics():
    topics = [_.topic_name for _ in Topic.query.all()]
    print(topics)
    return topics


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


@app.route('/act', methods=['GET', 'POST'])
def act():
    action = request.get_json()
    print(action)
    if action['action'] == 'start':
        print('in start')
        resp = GameController.start_game(action)
    elif action['action'] == 'next_card':
        print('in next')
        resp = GameController.next_card()
    elif action['action'] == 'prev_card':
        print('in prev')
        resp = GameController.prev_card()
    else:
        print('There is an action request error!')
        resp = None
    return jsonify(resp)


class GameController:
    used_cards = []
    consecutive_card_number = 0
    translem_ids = []

    @classmethod
    def start_game(cls, action):
        cls._clear_game()
        if not action['topics']:
            topics = ['origin']
        else:
            topics = action['topics']
        topic_ids = cls._get_id_for_topics(topics)
        cls.translem_ids = cls._get_translem_id(topic_ids)
        return cls.next_card()

    @classmethod
    def next_card(cls):
        if len(cls.used_cards) == cls.consecutive_card_number:
            resp = cls._get_new_card()
            cls.consecutive_card_number += 1
            cls.used_cards.append(resp)
        elif len(cls.used_cards) > cls.consecutive_card_number:
            resp = cls.used_cards[cls.consecutive_card_number]
            cls.consecutive_card_number += 1
        else:
            print('Unexpected operation for next_card', cls.consecutive_card_number, cls.used_cards)
            resp = None
        return resp

    @classmethod
    def prev_card(cls):
        if len(cls.used_cards) == 1 or cls.consecutive_card_number == 1:
            print("No cards have been played yet or shown is the last card")
            resp = cls.used_cards[cls.consecutive_card_number - 1]
        else:
            cls.consecutive_card_number -= 1
            resp = cls.used_cards[cls.consecutive_card_number - 1]
        return resp

    @staticmethod
    def _clear_game():
        __class__.used_cards = []
        __class__.consecutive_card_number = 0
        __class__.translem_ids = []

    @staticmethod
    def _get_new_card():
        random_translem_ids = __class__._get_random_8_translem_ids_from(__class__.translem_ids)
        russian_words, english_words = __class__._get_translems(random_translem_ids)
        resp = {'english': english_words, 'russian': russian_words}
        return resp

    @staticmethod
    def _get_id_for_topics(list_of_topics):
        return [db.session.query(Topic.id).filter(Topic.topic_name == topic).first()[0] for topic in list_of_topics]

    @staticmethod
    def _get_translem_id(topic_ids):
        translem_ids = []
        for topic_id in topic_ids:
            the_ids = db.session.query(Translems.id).filter(Translems.topic_id == topic_id).all()
            translem_ids.extend([value for (value,) in the_ids])
        return translem_ids

    @staticmethod
    def _get_random_8_translem_ids_from(translem_ids):
        return random.sample(translem_ids, 8)

    @staticmethod
    def _get_translems(translem_ids):
        russian = []
        english = []
        for id in translem_ids:
            translem = db.session.query(Translems.russian, Translems.english).filter(Translems.id == id).first()
            russian.append(translem[0])
            english.append(translem[1])
        print(russian, english)
        return russian, english
