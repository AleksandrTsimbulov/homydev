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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/act', methods=['GET', 'POST'])
def act():
    action = request.get_json()
    if action['action'] == 'start':
        print('in start')
        resp = start_game(action)
    elif action['action'] == 'next_card':
        print('in next')
        resp = gameController.next_card(action)
    elif action['action'] == 'prev_card':
        print('in prev')
        resp = gameController.prev_card(action)
    else:
        print('There is an action request error!')
        resp = None
    return jsonify(resp)


class gameController:



    def next_card(self, action):
        pass

    def prev_card(self, action):
        pass


def start_game(action):
    if not action['topics']:
        topics = ['origin']
    else:
        topics = action['topics']
    topic_ids = get_id_for_topics(topics)
    tranlem_ids = get_translem_id(topic_ids)
    random_translem_ids = get_random_8_translem_ids_from(tranlem_ids)
    russian_words, english_words = get_translems(random_translem_ids)
    resp = {'english': english_words, 'russian': russian_words}
    return resp


def get_id_for_topics(list):
    # returns list of chosen topic ids
    ids = []
    for topic in list:
        topic_id = db.session.query(Topic.id).filter(Topic.topic_name == topic).first()[0]
        ids.append(topic_id)
    print(ids)
    return ids


def get_translem_id(topic_ids):
    for topic_id in topic_ids:
        the_ids = db.session.query(Translems.id).filter(Translems.topic_id == topic_id).all()
        return [value for (value,) in the_ids]


def get_random_8_translem_ids_from(translem_ids):
    list_of_random_translems = random.sample(translem_ids, 8)
    return list_of_random_translems


def get_translems(translem_ids):
    russian = []
    english = []
    for id in translem_ids:
        translem = db.session.query(Translems.russian, Translems.english).filter(Translems.id == id).first()
        russian.append(translem[0])
        english.append(translem[1])
    print(russian, english)
    return russian, english
