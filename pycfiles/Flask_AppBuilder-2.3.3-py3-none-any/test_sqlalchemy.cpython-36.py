# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel/workarea/preset/Flask-AppBuilder/flask_appbuilder/tests/test_sqlalchemy.py
# Compiled at: 2020-03-31 08:10:13
# Size of source mod 2**32: 670 bytes
import unittest
from flask_appbuilder.models.sqla.interface import _is_sqla_type
from nose.tools import eq_
import sqlalchemy as sa

class CustomSqlaType(sa.types.TypeDecorator):
    impl = sa.types.DateTime(timezone=True)


class NotSqlaType:

    def __init__(self):
        self.impl = sa.types.DateTime(timezone=True)


class FlaskTestCase(unittest.TestCase):

    def test_is_sqla_type(self):
        t1 = sa.types.DateTime(timezone=True)
        t2 = CustomSqlaType()
        t3 = NotSqlaType()
        eq_(True, _is_sqla_type(t1, sa.types.DateTime))
        eq_(True, _is_sqla_type(t2, sa.types.DateTime))
        eq_(False, _is_sqla_type(t3, sa.types.DateTime))