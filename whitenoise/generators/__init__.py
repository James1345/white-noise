from whitenoise.generators.simple import * #Expose simple generators at this level

def generator(arg):
    if instanceof(arg, BaseGenerator):
        return arg
