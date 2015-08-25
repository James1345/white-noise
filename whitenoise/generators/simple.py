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

class SequenceGenerator(BaseGenerator):
    '''
    Creates a generator that yeilds the next object in sequence each time it is called

    If it runs out, it wraps back to the start.
    Any iterable may be passed as `values`
    '''
    def __init__(self, values):
        self.values = values
        self.iterator = iter(values)

    def generate(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.values)
            return next(self.iterator)

class ListGenerator(BaseGenerator):
    '''
    Creates a list of values by running another generator (or multiple generators)

    The entire list is assigned to a single instance of the model, not to be
    confused with SequenceGenerator which returns a single result each time
    it is run.
    '''

    def __init__(self, length, *generators):
        self.length=length
        self.generators = generators

    def __setattr__(self, field, value):
        '''
        Pass attribute settings through to children
        '''
        super().__setattr__(field, value)
        try:
            for generator in self.generators:
                setattr(generator, field, value)
        except:
            pass #Pass when generators does not exist

    def generate(self):
        iterator = iter(self.generators)
        retval = []
        for _ in range(self.length):
            try:
                val = next(iterator).generate()
            except StopIteration:
                iterator = iter(self.generators)
                val = next(iterator).generate()
            retval.append(val)
        return retval


class LiteralGenerator(BaseGenerator):
    def __init__(self, value=None):
        self.value = value

    def generate(self):
        return self.value
