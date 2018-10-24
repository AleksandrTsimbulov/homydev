from flask import render_template, flash, redirect, url_for, request, jsonify
from flask import abort
from alias import app, db
from alias.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from alias.models import User, Topic
from werkzeug.urls import url_parse

from alias.game_controller import GameController, CurrentGames

current_games = CurrentGames()


def create_game(user, controller):
    current_games.add_game(user, controller)


def remove_game(user):
    current_games.del_game(user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('welcome')

        create_game(current_user, GameController(current_user))

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    remove_game(current_user)
    logout_user()
    return redirect(url_for('welcome'))


@app.route('/act', methods=['POST'])
@login_required
def act():
    """
        {'action': possible_actions,
            'topics': [ chosen topics or None]}
            where possible_actions can be strings:
                'start',
                'next_card',
                'prev_card',
                'add_topics',
    """
    if request.method != 'POST':
        return abort(404)
    action = request.get_json()
    print(action)

    game_controller = current_games.get_game(current_user)
    if action['action'] == 'start':
        print('in start')
        resp = game_controller.start_game()
    elif action['action'] == 'add_topics':
        print('topics received')
        resp = game_controller.add_topics(action['topics'])
    elif action['action'] == 'next_card':
        print('in next')
        resp = game_controller.next_card()
    elif action['action'] == 'prev_card':
        print('in prev')
        resp = game_controller.prev_card()
    else:
        print('There is an action request error!')
        resp = None
    return jsonify(resp)


@app.route('/')
@app.route('/index')
@login_required
def index():
    topics = Topic.get_topic_names()
    return redirect(url_for('welcome'))
    # return render_template('welcome.html', topics=topics)


@app.route('/welcome')
def welcome():
    title = 'welcome'
    return render_template('welcome.html', title=title)


@app.route('/study')
def study():
    title = 'study'
    return render_template('study.html', title=title)


@app.route('/for_fun')
def for_fun():
    title = 'for fun'
    return render_template('for_fun.html', title=title)


@app.route('/game')
def game():
    title = 'game'
    return render_template('game.html', title=title)
