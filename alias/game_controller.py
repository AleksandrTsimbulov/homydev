import random
from datetime import datetime

from alias.models import Topic, Translems


class GameController:
    def __init__(self, user):
        self.creation_time = datetime.now()
        self._user = str(user)
        self.used_cards = []
        self.order_card_number = 0
        self.translem_ids = []
        self.topics = []

    @property
    def user(self):
        return self._user

    def start_game(self, action):
        self.clear_game()
        if not action['topics']:
            topics = ['original']
        else:
            topics = action['topics']
        self.topics = topics
        topic_ids = self._get_id_for_topics(self.topics)
        self.translem_ids = self._get_translem_id(topic_ids)
        return self.next_card()

    def next_card(self):
        if len(self.used_cards) == self.order_card_number:
            resp = self._get_new_card()
            self.order_card_number += 1
            self.used_cards.append(resp)
        elif len(self.used_cards) > self.order_card_number:
            resp = self.used_cards[self.order_card_number]
            self.order_card_number += 1
        else:
            print('Unexpected operation for next_card', self.order_card_number, self.used_cards)
            resp = None
        return resp

    def prev_card(self):
        if len(self.used_cards) == 1 or self.order_card_number == 1:
            print("No cards have been played yet or shown is the last card")
            resp = self.used_cards[self.order_card_number - 1]
        else:
            self.order_card_number -= 1
            resp = self.used_cards[self.order_card_number - 1]
        return resp

    def clear_game(self):
        self.used_cards = []
        self.order_card_number = 0
        self.translem_ids = []

    def _get_id_for_topics(self, list_of_topics):
        return [Topic.get_id_by_name(topic) for topic in list_of_topics]

    def _get_new_card(self):
        if len(self.translem_ids) <= 8:
            topic_ids = self._get_id_for_topics(self.topics)
            self.translem_ids = self._get_translem_id(topic_ids)
        random_translem_ids = self._get_random_8_translem_ids_from(self.translem_ids)
        russian_words, english_words = self._get_translems(random_translem_ids)
        return {'english': english_words, 'russian': russian_words}

    def _get_translem_id(self, topic_ids):
        translem_ids = []
        for topic_id in topic_ids:
            translem_ids.extend(Translems.get_ids_by_topic_id(topic_id))
        return translem_ids

    def _get_random_8_translem_ids_from(self, translem_ids):
        return random.sample(translem_ids, 8)

    def _get_translems(self, translem_ids):
        russian = []
        english = []
        for translem_id in translem_ids:
            russian.append(Translems.get_russian(translem_id))
            english.append(Translems.get_english(translem_id))
        print(russian, english)
        return russian, english


class CurrentGames:
    def __init__(self):
        self.games = {}

    def add_game(self, username, game_controller):
        self.games[str(username)] = game_controller
        self._remove_old()

    def del_game(self, username):
        username = str(username)
        if username in self.games:
            del self.games[username]
        self._remove_old()

    def _remove_old(self):
        current_time = datetime.now()
        for key in list(self.games.keys()):
            age = current_time - self.games[key].creation_time
            if age.seconds > 18000:
                del self.games[key]

    def get_game(self, username):
        username = str(username)
        if username in self.games.keys():
            return self.games[username]
        else:
            self.add_game(username, GameController(username))
            return self.games[username]
