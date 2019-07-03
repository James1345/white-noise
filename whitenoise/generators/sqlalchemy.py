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
    def __init__(self, model, random=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.model = model
        self.random = random

    def generate(self):
        if(self.session is None):
            raise ValueError('You must set the session property before using this generator')
        _query = self.session.query(self.model).all()
        if self.random:
            return random.SystemRandom().choice(_query)
        else:
            return _query[0]

class LinkGenerator(BaseGenerator):
    '''
    Creates a list for secondary relationships using link tables by selecting from another SQLAlchemy table
    Depends on SQLAlchemy, and receiving a session object from the Fixture runner
    the SQLAlchemy fixture runner handles this for us
    Receives the name of another class to lookup and max_map determines the maximum number of
    associations to create (default is 1)
    If the query returns more than one option, either random or the 1st is selected
    (default is random)
    '''
    _query = []
    _chosen_map = []

    def __init__(self, model, max_map=1, unique_maps=False, random=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.model = model
        self.random = random
        self.max_map = max_map 
        self.unique_maps = unique_maps

    def generate(self):
        if(self.session is None):
            raise ValueError('You must set the session property before using this generator')
        if not LinkGenerator._query:
            LinkGenerator._query = self.session.query(self.model).all()
        if self.random:
            if self.unique_maps:
                while True:
                    iterList = random.SystemRandom().sample(LinkGenerator._query,random.randint(1, self.max_map))
                    iterCheck = any(elem in iterList for elem in LinkGenerator._chosen_map)
                    if not iterCheck:
                        LinkGenerator._chosen_map.extend(iterList)
                        break
                return iterList 
            else:
                return random.SystemRandom().sample(LinkGenerator._query,random.randint(1, self.max_map))
        else:
            return [LinkGenerator._query[0]]