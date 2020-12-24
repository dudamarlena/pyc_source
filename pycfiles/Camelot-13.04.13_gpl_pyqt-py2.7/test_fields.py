# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_orm/test_fields.py
# Compiled at: 2013-04-11 17:47:52
"""
test the different syntaxes to define fields
"""
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