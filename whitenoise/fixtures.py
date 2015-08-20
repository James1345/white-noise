
class Fixture:
    '''
    Fixture takes the name of a model to act on,
    a list of dependancies, a number of items,
    and a dict of fields and generators
    '''

    def __init__(self, dependancies, model, quantity, fields):
        self.dependancies = dependancies
        self.model = model
        self.quantity = quantity
        self.fields = fields

class CircularDependancyException(Exception):
    pass

class DependancyResolver:
    '''
    Resolves dependencies, obviously
    '''
    def __init__(self, fixtures):
        self.fixtures = fixtures

    def recurse_resolve(node, resolved, unresolved):
        if node not in resolved:
            unresolved.append(node)
            for edge in node.dependencies:
                if edge in unresolved:
                    raise CircularDependancyException("Circular dependancy detected %s" % edge)
                recurse_resolve(edge, resolved, unresolved)
            unresolved.remove(node)
            resolved.append(node)

    def get_ordered_set():
        resolved = []
        unresolved = []
        for fixture in self.fixtures:
            recurse_resolve(fixture, resolved, unresolved)
        return resolved


class FixtureRunner:
    '''
    Takes a list of Fixtures and runs them on the specified connection
    '''

    def __init__(self, fixtures):

        self.fixtures = DependancyResolver(fixtures).get_ordered_set()
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

    def apply_fixture(self, fixture):
        for _ in range(fixture.quantity):
            model_instance = fixture.model()
            for field, (generator, options) in fixture.fields:
                setattr(model_instance, field, generator(**options).generate)
            self.session.add(model_instance)
            self.session.commit()
