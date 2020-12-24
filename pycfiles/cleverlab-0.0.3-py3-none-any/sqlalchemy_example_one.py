# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/project/+package+/models/sqlalchemy_example_one.py
# Compiled at: 2006-08-02 05:57:51
from sqlalchemy import *
from sqlalchemy.schema import default_metadata as metadata
person_table = Table('person', metadata, Column('person_id', Integer, primary_key=True), Column('person_name', String(16)), Column('password', String(20)))
address_table = Table('address', metadata, Column('address_id', Integer, primary_key=True), Column('person_id', Integer, ForeignKey('person.person_id')), Column('street', String(100)), Column('city', String(80)), Column('state', String(2)), Column('zip', String(10)))

class Person(object):
    __module__ = __name__

    def __init__(self, person_name, password):
        self.person_name = person_name
        self.password = password

    def __str__(self):
        return 'Person: %s' % (self.person_name,)


class Address(object):
    __module__ = __name__

    def __init__(self, street, city, state, zip):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip


person_mapper = mapper(Person, person_table, properties=dict(addresses=relation(Address)))
address_mapper = mapper(Address, address_table)