from flask import request, abort, redirect, flash, render_template, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from alias.game_controller import GameController, CurrentGames
from alias.models import User
from alias.forms import LoginForm
from alias import app
from werkzeug.urls import url_parse

current_games = CurrentGames()


def create_game(user, controller):
    current_games.add_game(user, controller)


def remove_game(user):
    current_games.del_game(user)


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

        create_game(current_user, GameController(current_user))

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():

    remove_game(current_user)

    logout_user()
    return redirect(url_for('index'))


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
    """
    if request.method != 'POST':
        return abort(404)
    action = request.get_json()
    print(action)
    game_controller = current_games.get_game(current_user)
    if action['action'] == 'start':
        print('in start')
        resp = game_controller.start_game(action)
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
