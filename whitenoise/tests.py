from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from whitenoise.fixtures import SQLAlchemyFixtureRunner, Fixture
from whitenoise.generators import RandomGenerator

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class SQLAlchemyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        cls.session = sessionmaker(bind=engine)()

    def testFixtures(self):
        fixtures = [
            Fixture(
                dependencies = [],
                model = User,
                quantity = 6,
                fields = {
                    'name': (RandomGenerator, {}),
                }
            )
        ]
        SQLAlchemyFixtureRunner(self.session, fixtures).run()
        for instance in self.session.query(User):
            print(instance.name)
