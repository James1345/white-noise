from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

from whitenoise.fixtures import SQLAlchemyFixtureRunner, Fixture
from whitenoise.generators import LiteralGenerator, SequenceGenerator, sqlalchemy, ListGenerator
from whitenoise.shortcuts import RANDOM, INSULT

import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('adresses', order_by=id))

    def __repr__(self):
        return "<Address - id:%d user_id:%d>" % (self.id, self.user_id)

random_user = Fixture(
        dependencies = [],
        model = User,
        quantity = 6,
        fields = {
            'name': RANDOM,
        }
    )

insult_user = {
    'model': User,
    'quantity': 3,
    'fields': {
        'name': INSULT,
    }
}

literal_user = Fixture(
        dependencies = [],
        model = User,
        quantity = 4,
        fields = {
            'name': 'Hello World',
        }
    )

sequenced_user = Fixture(
        dependencies = [random_user, literal_user],
        model = User,
        quantity = 4,
        fields = {
            'name': ['Alice', 'Bob', 'Charlie', lambda: 'Danny'],
        }
)

user_address = Fixture(
    dependencies = [sequenced_user],
    model = Address,
    quantity = 1,
    fields = {
        'user': sqlalchemy.SelectGenerator(model=User) #select a random user
    }
)

blank_address = Fixture(
    dependencies = [],
    model = Address,
    quantity = 1,
    fields = {}
)

back_user = Fixture(
    dependencies = [blank_address],
    model = User,
    quantity = 1,
    fields = {
        'name': 'Back User',
        'adresses': ListGenerator(1, (sqlalchemy.SelectGenerator(model=Address),))
    }
)

uuid_user = Fixture(
    dependencies = [],
    model = User,
    quantity = 1,
    fields = {
        'name': lambda: str(uuid.uuid4())
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
            back_user,
            sequenced_user,
            random_user,
            literal_user,
            insult_user,
            user_address,
            uuid_user,
        ]
        SQLAlchemyFixtureRunner(self.session, fixtures).run()

        for instance in self.session.query(User):
            print(instance.name)
        for instance in self.session.query(Address):
            print(instance)
