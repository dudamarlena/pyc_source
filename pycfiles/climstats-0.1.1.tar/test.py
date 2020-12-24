# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/takumakanari/develop/my/py-projects/climson_dev/climson/tests/test.py
# Compiled at: 2013-09-21 21:58:10
import nose
from nose.tools import ok_, eq_, raises
from climson import ClimsonClient
from climson.climson import BaseCommand, ClimsonException, ValidateError, make_option

class TestCommand(BaseCommand):
    name = 'test'
    description = 'description'
    options = BaseCommand.options + (
     make_option('--message', dest='message'),
     make_option('--age', dest='age', type=int))

    def do_command(self, message=None, age=0):
        return (
         message, age)

    def validate(self, message=None, age=0):
        if age < 10:
            return False
        return True


class TestClimsonClient(object):

    def __init__(self):
        self.client = ClimsonClient(prog=str(self), description='test')

    def test_add(self):
        ret = self.client.add(TestCommand)
        ok_(ret is not None)
        return

    @raises(ClimsonException)
    def test_add_invalid_type(self):
        self.client.add(str)

    def test_execute(self):
        self.client.add(TestCommand)
        ret = self.client.execute(args=['test', '--message', 'ok', '--age', '10'])
        ok_(ret is not None)
        eq_(ret[0], 'ok')
        eq_(ret[1], 10)
        return

    @raises(ValidateError)
    def test_validate(self):
        self.client.add(TestCommand)
        ret = self.client.execute(args=['test', '--message', 'ok', '--age', '9'])