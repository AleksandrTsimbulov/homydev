from random import random
from datetime import datetime

from alias import db
from alias.models import User, Topic, Translems


class GameController:
    def __init__(self, user):
        self.creation_time = datetime.now()
        self._user = user
        self.used_cards = []
        self.consecutive_card_number = 0
        self.translem_ids = []

    @property
    def user(self):
        return self._user

    def start_game(self, action):
        self.clear_game()
        if not action['topics']:
            topics = ['original']
        else:
            topics = action['topics']
        topic_ids = self._get_id_for_topics(topics)
        self.translem_ids = self._get_translem_id(topic_ids)
        return self.next_card()

    def next_card(self):
        if len(self.used_cards) == self.consecutive_card_number:
            resp = self._get_new_card()
            self.consecutive_card_number += 1
            self.used_cards.append(resp)
        elif len(self.used_cards) > self.consecutive_card_number:
            resp = self.used_cards[self.consecutive_card_number]
            self.consecutive_card_number += 1
        else:
            print(print('Unexpected operation for next_card', self.consecutive_card_number, self.used_cards))
            resp = None
        return resp

    def prev_card(self):
        if len(self.used_cards) == 1 or self.consecutive_card_number == 1:
            print("No cards have been played yet or shown is the last card")
            resp = self.used_cards[self.consecutive_card_number - 1]
        else:
            self.consecutive_card_number -= 1
            resp = self.used_cards[self.consecutive_card_number - 1]
        return resp

    def clear_game(self):
        self.used_cards = []
        self.consecutive_card_number = 0
        self.translem_ids = []

    def _get_id_for_topics(self, list_of_topics):
        return [Topic.get_id_by_name(topic) for topic in list_of_topics]

    def _get_new_card(self):
        random_translem_ids = self._get_random_8_translem_ids_from(self.translem_ids)
        russian_words, english_words = self._get_translems(random_translem_ids)
        resp = {'english': english_words, 'russian': russian_words}
        return resp

    def _get_translem_id(self, topic_ids):
        translem_ids = []
        for topic_id in topic_ids:
            the_ids = db.session.query(Translems.id).filter(Translems.topic_id == topic_id).all()
            translem_ids.extend([value for (value,) in the_ids])
        return translem_ids

    def _get_random_8_translem_ids_from(self, translem_ids):
        return random.sample(translem_ids, 8)

    def _get_translems(self, translem_ids):
        russian = []
        english = []
        for id in translem_ids:
            translem = db.session.query(Translems.russian, Translems.english).filter(Translems.id == id).first()
            russian.append(translem[0])
            english.append(translem[1])
        print(russian, english)
        return russian, english


class CurrentGames:
    def __init__(self):
        self.games = {}

    def add_game(self, username, game_controller):
        self.games[username] = game_controller
        self._remove_old()

    def del_game(self, username):
        if username in self.games:
            del self.games[username]
        self._remove_old()

    def _remove_old(self):
        current_time = datetime.now()
        for key in list(self.games.keys()):
            age = current_time - self.games[key].creation_time
            if age.seconds > 18000:
                del self.games[key]

