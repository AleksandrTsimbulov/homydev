from extracter import ecxeltranslemreader
from alias import db
from alias.models import Topic, Translems


class DbLoader:
    '''
    Load translems from excel.xlsx document to an existed database
    Every single file must have it's 'topic' at specified position and
    russian/english phrases since specified row in columns A and B
    '''
    def __init__(self, filename):
        reader = ecxeltranslemreader.ExcelExtractor(filename)
        self._topic = reader.get_topic()
        self._translems = reader.get_translems()
        print(self._topic)
        print(self._translems)

    def _load_topic(self):
        try:
            topic_id = Topic.query.filter(Topic.topic_name == self._topic).first().id
        except Exception as exp:
            print('in _load_topic exceptions', exp)
            topic_id = 'Some weird id'
        if not topic_id:
            db.session.add(Topic(topic_name=self._topic))
        else:
            print(f'Looks like you have already had this {self._topic} in your db')
            exit()

    def _load_tranlems(self, topic_id):
        for translem in self._translems:
            db.session.add(Translems(russian=translem[1], english=translem[0], topic_id=topic_id))

    def load_translems(self):
        try:
            self._load_topic()
        except Exception as e:
            print('Load topic exceptions', e)
        topic_id = Topic.query.filter(Topic.topic_name == self._topic).first().id
        print(topic_id)
        try:
            self._load_tranlems(topic_id)
        except Exception as e:
            print('Translems load exception', e)
        db.session.commit()


if __name__ == '__main__':
    db_loader = DbLoader('../extracter/Translems.xlsx')
    db_loader.load_translems()
