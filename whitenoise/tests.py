from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from whitenoise.fixtures import SQLAlchemyFixtureRunner, Fixture
from whitenoise.generators import RandomGenerator, InsultGenerator, LiteralGenerator, SequenceGenerator

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

random_user = Fixture(
        dependencies = [],
        model = User,
        quantity = 6,
        fields = {
            'name': RandomGenerator(),
        }
    )

insult_user = Fixture(
        dependencies = [],
        model = User,
        quantity = 3,
        fields = {
            'name': InsultGenerator(),
        }
    )

literal_user = Fixture(
        dependencies = [],
        model = User,
        quantity = 4,
        fields = {
            'name': LiteralGenerator(value='Hello World'),
        }
    )

sequenced_user = Fixture(
        dependencies = [random_user, literal_user],
        model = User,
        quantity = 4,
        fields = {
            'name': SequenceGenerator(values=['Alice', 'Bob', 'Charlie']),
        }
)

class SQLAlchemyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        cls.session = sessionmaker(bind=engine)()

    def testFixtures(self):
        fixtures = [
            sequenced_user,
            random_user,
            literal_user,
            insult_user,
        ]
        SQLAlchemyFixtureRunner(self.session, fixtures).run()
        for instance in self.session.query(User):
            print(instance.name)
