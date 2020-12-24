# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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