import inspect

def generator(arg):
    '''
    Takes an argument and converts it to a generator

    If a generator is passed it is returned. A generator is defined as a subclass
    of BaseGenerator, or any object with a #generate method that takes no
    arguments (other than 'self')

    If an argument other than a generator is passed, an appropriate generator
    from the simple generators is selected to wrap it, using the following
    list (in order of precedence)

    - generator passed => return arg
    - String literal => LiteralGenerator[#]_
    - callable object (no args) => FunctionGenerator
    - iterable object => SequenceGenerator
    - other object => LiteralGenerator(str(object))

    .. [#] Strings are handled first, as they are also iterable, but it is
       more likely that they are wanted as Literals, not sequences of Chars
    '''

    ## Import is in the function to avoid circular problems
    from whitenoise.generators.simple import LiteralGenerator, FunctionGenerator, BaseGenerator
    from whitenoise.generators.list import SequenceGenerator

    if isinstance(arg, BaseGenerator):
        return arg
    try:
        if callable(arg.generate) and inspect.getargspec(arg.generate).args == ['self',]:
            return arg
        else:
            # generate exists, but has more arguments, pass over it
            # and test if it matches any other specs
            pass
    except AttributeError:
        # No such method, continue
        pass

    if isinstance(arg, str):
        return LiteralGenerator(arg)
    if callable(arg) and inspect.getargspec(arg).args == []:
        return FunctionGenerator(arg)
    try:
        return SequenceGenerator(arg)
    except TypeError:
        #Object is not iterable, pass
        pass
    return LiteralGenerator(str(arg))
