import inspect
from whitenoise.generators import FunctionGenerator, LiteralGenerator

class Fixture:
    '''
    Fixture takes the name of a model to act on,
    a list of dependancies, a number of items,
    and a dict of fields and generators
    '''

    def __init__(self, dependencies, model, quantity, fields):
        self.dependencies = dependencies
        self.model = model
        self.quantity = quantity
        self.fields = self.compile_fields(fields)

    def compile_fields(self, fields):
        '''
        Shortcut helper.
        This method inspects the parameter passed to the field, and constructs
        an appropriate generator for it

        If a generator is passed, it is assigned. If a function that can be
        called without arguments is assigned, FunctionGenerator is used, otherwise
        a LiteralGenerator is constructed.
        '''
        retval = {}
        for key, value in fields.items():
            try:
                callable(value.generate)
                retval[key] = value
            except AttributeError:
                if callable(value):
                    argspec = inspect.getargspec(value)
                    if len(argspec.args) == 0 or (len(argspec.args) == len(argspec.defaults)):
                        retval[key] = FunctionGenerator(value)
                    else:
                        raise ValueError("Function must be callable with no args to use this way")
                else:
                    retval[key] = LiteralGenerator(value)
        return retval

class CircularDependancyException(Exception):
    pass

class DependencyResolver:
    '''
    Resolves dependencies, obviously
    '''
    def __init__(self, fixtures):
        self.fixtures = fixtures

    def recurse_resolve(self, node, resolved, unresolved):
        if node not in resolved:
            unresolved.append(node)
            for edge in node.dependencies:
                if edge in unresolved:
                    raise CircularDependancyException("Circular dependancy detected %s" % edge)
                self.recurse_resolve(edge, resolved, unresolved)
            unresolved.remove(node)
            resolved.append(node)

    def get_ordered_set(self):
        resolved = []
        unresolved = []
        for fixture in self.fixtures:
            self.recurse_resolve(fixture, resolved, unresolved)
        return resolved


class FixtureRunner:
    '''
    Takes a list of Fixtures and runs them on the specified connection
    '''

    def __init__(self, fixtures):

        self.fixtures = DependencyResolver(fixtures).get_ordered_set()
        if type(self) == FixtureRunner:
            # Disallow creation of the base class
            raise NotImplementedError("FixtureRunner MUST be subclassed")

    def run(self):
        for fixture in self.fixtures:
            self.apply_fixture(fixture)

    def apply_fixture(self, fixture):
        raise NotImplementedError()

class SQLAlchemyFixtureRunner(FixtureRunner):

    def __init__(self, session, fixtures):
        super().__init__(fixtures)
        self.session = session
        self.session.autoflush = False

    def apply_fixture(self, fixture):
        for _ in range(fixture.quantity):
            model_instance = fixture.model()
            for field, generator in fixture.fields.items():
                generator.session = self.session
                setattr(model_instance, field, generator.generate())
            self.session.add(model_instance)
            self.session.flush()
            self.session.commit()

class DjangoFixtureRunner(FixtureRunner):
    def apply_fixture(self, fixture):
        for _ in range(fixture.quantity):
            model_instance = fixture.model()
            for field, (generator, options) in fixture.fields.items():
                setattr(model_instance, field, generator.generate())
            model_instance.save()
