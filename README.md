# white-noise

Test Data generator for SQLAlchemy (and possibly Django)

This package is designed to make it easy to generate test data for SQLAlchemy
applications (Django possibly to come in the future). It was inspired after spending
most of a day failing to get Mixer working properly.

The aim is to have a (mostly) consistant api for all generation.

## API overview
Fixtures define the data that should be entered into the database. Generators
create the data and a fixture runner enters it.

A fixture object takes 4 parameters.

- *model* The model to be acted on. This
should be a direct reference to the model class that data should be created for.

- *quantity* How many instances of the model need adding to the database

- *dependancies* A list of fixtures that this fixture depends on. The base for fixture runners can resolve dependancies to ensure fixtures are ruin in the correct order

- *fields* This is a dictionary of field names to tuples. The field name is the field of the model to be generated, the tuple is of the form (generator, options), where generator is a generator class and options is a dictionary of options to pass to the generator's
