# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/tests/test_model_form.py
# Compiled at: 2014-11-07 07:51:00
import unittest
from pyck.forms import model_form
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(Text, primary_key=True, nullable=False, default='admin')
    password = Column(Text, nullable=False)


class TestModelForm(unittest.TestCase):

    def setUp(self):
        UserForm = model_form(User)
        self.myform = UserForm()

    def tearDown(self):
        pass

    def test_01_properties_test(self):
        assert hasattr(self.myform, 'username')
        assert hasattr(self.myform, 'password')

    def test_02_has_as_p(self):
        assert hasattr(self.myform, 'as_p')
        assert callable(self.myform.as_p)

    def test_03_has_as_table(self):
        assert hasattr(self.myform, 'as_table')
        assert callable(self.myform.as_table)