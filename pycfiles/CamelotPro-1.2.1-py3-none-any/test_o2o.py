# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_orm/test_o2o.py
# Compiled at: 2013-04-11 17:47:52
from . import TestMetaData
from camelot.core.orm import Field, OneToOne, ManyToOne
from sqlalchemy.types import String, Unicode, Integer

class TestOneToOne(TestMetaData):

    def test_simple(self):

        class A(self.Entity):
            name = Field(String(60))
            b = OneToOne('B')

        class B(self.Entity):
            name = Field(String(60))
            a = ManyToOne('A')

        self.create_all()
        with self.session.begin():
            b1 = B(name='b1', a=A(name='a1'))
        self.session.expire_all()
        b = B.query.one()
        a = b.a
        assert b == a.b