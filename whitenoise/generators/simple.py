### Generators that are database agnostic and very simple

from insultgenerator.phrases import get_so_insult_with_action_and_target
from loremipsum import get_sentence

from whitenoise.random import random_string

class BaseGenerator:
    def __init__(self, *args, **kwargs):
        pass #ignore superfluous args

    def generate(self):
        raise NotImplementedError("Must be implemented by subclass")

class InsultGenerator(BaseGenerator):
    def generate(self):
        return get_so_insult_with_action_and_target('Yo Moma', 'she')

class RandomGenerator(BaseGenerator):
    def __init__(self, length=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length

    def generate(self):
        return random_string(self.length)

class LipsumGenerator(BaseGenerator):
    def generate(self):
        return get_sentence(True)

class SequenceGenerator(BaseGenerator):
    '''
    Creates a generator that yeilds the next object in sequence each time it is called

    If it runs out, it wraps back to the start.
    Any iterable may be passed as `values`
    '''
    def __init__(self, values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = values
        self.iterator = iter(self.values)

    def generate(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.values)
            return next(self.iterator)


class LiteralGenerator(BaseGenerator):
    def __init__(self, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def generate(self):
        return self.value
