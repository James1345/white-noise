# white-noise
[![Build Status](https://travis-ci.org/James1345/white-noise.svg?branch=feature%2Fdjango-management-command)](https://travis-ci.org/James1345/white-noise)

Test Data generator for SQLAlchemy and Django

This package is designed to make it easy to generate test data for SQLAlchemy
or Django applications. It was inspired after spending
most of a day failing to get Mixer working properly.

The aim is to have a consistant, simple API for all generation.

## API overview
Fixtures define the data that should be entered into the database. Generators
create the data and a fixture runner enters it.

### Fixtures

A fixture object takes 4 parameters.

- **model** The model to be acted on. This
should be a direct reference to the model class that data should be created for.

- **quantity** How many instances of the model need adding to the database

- **dependencies** A list of fixtures that this fixture depends on. The base for fixture runners can resolve dependencies to ensure fixtures are ruin in the correct order

- **fields** This is a dictionary of field names to generator instances. The field name is the field of the model to be generated, where generator is a generator to be used (it is normal to instansiate the generator in the fields list)

### Generators

Currently available generators (and their options)

#### LiteralGenerator

Returns a literal value that is passed

- **value** The value to return

#### RandomGenerator

Creates a random string for the field

- **length** The length of the field

#### LipsumGenerator

Creates a semi-random string sentence of the Lorem Ipsum form

#### InsultGenerator

Creates a random insulting sentence  string for the field

#### SequenceGenerator

Iterates over a sequence. Loops if the end of the sequence is reached.

- **values** The values to use. Can be any iterable (lists, tuples, generators, etc.)

#### sqlalchemy.SelectGenerator
Selects an object from the database and uses that as the value for the field
This is for creating objects with relationships to others in the database (e.g. foreign keys)

This generator only works with the SQLAlchemy fixture runner. (if writting your own fixture runner
it must receive an SQLAlchemy session object as well as its options)

- **model** The foreign model to select from

- **random** Select randomly or select the first (default => random)


### Fixture runners

#### SQLAlchemyFixtureRunner

Runs the fixtures using SQLAlchemy models. This class must be instantiated with
a reference to a SQLAlchemy session object to be used for accessing the database

#### DjangoFixtureRunner

Runs the fixtures against a Django database. It must be run in a django context
(e.g. from a custom management command)

A Django management command is included. To use it, add `'whitenoise'` to your
installed apps
