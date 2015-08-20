from insultgenerator.phrases import get_so_insult_with_action_and_target
from loremipsum import get_sentence

from whitenoise.random import random_string

# Conveinience functins
def lipsum():
    return get_sentence(True)

def insult():
    return get_so_insult_with_action_and_target('Yo Moma', 'she')

class BaseGenerator:
    def generate(self):
        raise NotImplementedError("Must be implemented by subclass")

class InsultGenerator(BaseGenerator):
    def generate():
        return insult()

class RandomGenerator(BaseGenerator):
    def __init__(self, length=10):
        self.length = length

    def generate(self):
        return random_string(self.length)
