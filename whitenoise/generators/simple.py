### Generators that are database agnostic and very simple

from insultgenerator.phrases import get_so_insult_with_action_and_target
from loremipsum import get_sentence

from whitenoise.random import random_string

class BaseGenerator:
    def __init__(self):
        pass #ignore superfluous args

    def generate(self):
        raise NotImplementedError("Must be implemented by subclass")

class FunctionGenerator(BaseGenerator):
    '''
    Generator that takes a function and runs it once per call to
    #generate.

    The extra arguments will be passed to the function when it is called
    '''

    def __init__(self, function, *function_args, **function_kwargs):
        self.function = function
        self.function_args = function_args
        self.function_kwargs = function_kwargs

    def generate(self):
        return self.function(*self.function_args, **self.function_kwargs)

def InsultGenerator():
    '''
    Insult generator

    So specific it can actually be managed as an instance of function generator
    '''
    return FunctionGenerator(get_so_insult_with_action_and_target, 'Yo Moma', 'she')

class RandomGenerator(FunctionGenerator):
    '''
    Uses function generator to create a random string of the given length
    '''
    def __init__(self, length):
        super().__init__(random_string, length)

def LipsumGenerator():
    '''
    Lorem Ipsum generator

    So specific it can actually be managed as an instance of function generator
    '''
    return FunctionGenerator(get_sentence, True)

class LiteralGenerator(BaseGenerator):
    def __init__(self, value=None):
        self.value = value

    def generate(self):
        return self.value
