import random
from whitenoise.generators import BaseGenerator

class SelectGenerator(BaseGenerator):
    '''
    Creates a value by selecting from another SQLAlchemy table
    Depends on SQLAlchemy, and receiving a session object from the Fixture runner
    the SQLAlchemy fixture runner handles this for us
    Receives the name of another class to lookup. If the
    query returns more than one option, either random or the 1st is selected
    (default is random)
    '''
    def __init__(self, session=None, model, random=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        self.model = model
        self.random = random

    def generate(self):
        _query = session.query(model).all()
        if self.random:
            return random.SystemRandom().choice(_query)
        else:
            return _query[0]
