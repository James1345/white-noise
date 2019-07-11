import random
from whitenoise.generators import BaseGenerator
from sqlalchemy.inspection import inspect

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
    unique_maps will ensure no association used in a prior object creation is used for a new instance. (Default is False)
    max_iter will ensure no infinite loop searching for unique map. To be used in combination with unique_maps and has no effect otherwise
    (default max_iter=100)
    If the query returns more than one option, either random or the 1st is selected
    (default is random)
    '''
    _query = {}
    _chosen_map = {}

    def __init__(self, model, max_map=1, unique_maps=False, max_iter=100, random=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.model = model
        self.random = random
        self.max_map = max_map 
        self.unique_maps = unique_maps
        self.max_iter = max_iter

    def generate(self):
        if(self.session is None):
            raise ValueError('You must set the session property before using this generator')
        if not self.model in LinkGenerator._query.keys():
            LinkGenerator._query[self.model] = self.session.query(self.model).all()
        if self.random:
            if self.unique_maps:
                if(self.max_iter <= 0):
                    raise ValueError('You must set max_iter to a valid integer >= 0')
                while (self.max_iter > 0):
                    iterExists = False
                    iterList = random.SystemRandom().sample(LinkGenerator._query[self.model],random.randint(1, self.max_map))
                    pkList = []
                    for elem in iterList:
                        pkList.append(inspect(elem).identity)
                    if self.model in LinkGenerator._chosen_map.keys():
                        iterExists = any(elem in pkList for elem in LinkGenerator._chosen_map[self.model])
                        if not iterExists:
                            LinkGenerator._chosen_map[self.model].extend(pkList)
                            break
                    else:
                        LinkGenerator._chosen_map[self.model] = pkList
                        break
                    iterList = []
                    self.max_iter = self.max_iter - 1
                if iterList:
                    return iterList
                else:
                    raise RuntimeError('Max iterations exceeded searching unique maps for ' + str(self.model))
            else:
                return random.SystemRandom().sample(LinkGenerator._query[self.model],random.randint(1, self.max_map))
        else:
            return [LinkGenerator._query[self.model][0]]
