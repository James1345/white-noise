from whitenoise.generators.generator import generator
from whitenoise.generators.simple import BaseGenerator

class BaseListGenerator(BaseGenerator):
    '''
    Superclass for generators that operate on lists
    '''

    def __init__(self, values):
        self.list = values
        self._make_generator_list()

    def _make_generator_list(self):
        retval = []
        for item in self.list:
            retval.append(generator(item))
        self.list = retval

    def __setattr__(self, field, value):
        '''
        Pass attribute settings through to children
        '''
        super().__setattr__(field, value)
        try:
            for item in self.list:
                setattr(item, field, value)
        except:
            pass #Pass when list does not exist


class SequenceGenerator(BaseListGenerator):
    '''
    Creates a generator that yeilds the next object in sequence each time it is called

    If it runs out, it wraps back to the start.
    Any iterable may be passed as `values`

    values in the sequence are converted into generators as per the rules defined
    in #generator
    '''
    def __init__(self, values):
        super().__init__(values)
        self.iterator = iter(self.list)

    def generate(self):
        try:
            return next(self.iterator).generate()
        except StopIteration:
            self.iterator = iter(self.list)
            return next(self.iterator).generate()

class ListGenerator(BaseListGenerator):
    '''
    Creates a list of values

    The entire list is assigned to a single instance of the model, not to be
    confused with SequenceGenerator which returns a single result each time
    it is run.

    Like SequenceGenerator each value in the passed list is converted to a
    generator and called
    '''

    def __init__(self, length, values):
        self.length=length
        super().__init__(values)

    def generate(self):
        iterator = iter(self.list)
        retval = []
        for _ in range(self.length):
            try:
                val = next(iterator).generate()
            except StopIteration:
                iterator = iter(self.list)
                val = next(iterator).generate()
            retval.append(val)
        return retval
