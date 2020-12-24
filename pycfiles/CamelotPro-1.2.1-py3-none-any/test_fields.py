# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_orm/test_fields.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\ntest the different syntaxes to define fields\n'
from . import TestMetaData
from camelot.core.orm import Field, has_field
from sqlalchemy.types import String

class TestFields(TestMetaData):

    def test_attr_syntax(self):

        class Person(self.Entity):
            firstname = Field(String(30))
            surname = Field(String(30))

        self.create_all()
        self.session.begin()
        Person(firstname='Homer', surname='Simpson')
        Person(firstname='Bart', surname='Simpson')
        self.session.commit()
        self.session.expunge_all()
        p = Person.get_by(firstname='Homer')
        assert p.surname == 'Simpson'

    def test_has_field(self):

        class Person(self.Entity):
            has_field('firstname', String(30))
            has_field('surname', String(30))

        self.create_all()
        self.session.begin()
        Person(firstname='Homer', surname='Simpson')
        Person(firstname='Bart', surname='Simpson')
        self.session.commit()
        self.session.expunge_all()
        p = Person.get_by(firstname='Homer')
        assert p.surname == 'Simpson'