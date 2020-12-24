# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/regrtest_data/dummy_plugin/dummy_plugin.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 788 bytes
from pylint.checkers import BaseChecker

class DummyPlugin1(BaseChecker):
    name = 'dummy_plugin'
    msgs = {'I9061': ('Dummy short desc 01', 'dummy-message-01', 'Dummy long desc')}
    options = (
     (
      'dummy_option_1',
      {'type':'string', 
       'metavar':'<string>', 
       'help':'Dummy option 1'}),)


class DummyPlugin2(BaseChecker):
    name = 'dummy_plugin'
    msgs = {'I9060': ('Dummy short desc 02', 'dummy-message-02', 'Dummy long desc')}
    options = (
     (
      'dummy_option_2',
      {'type':'string', 
       'metavar':'<string>', 
       'help':'Dummy option 2'}),)


def register(linter):
    linter.register_checker(DummyPlugin1(linter))
    linter.register_checker(DummyPlugin2(linter))