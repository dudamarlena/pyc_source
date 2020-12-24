# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/Action_test.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 2054 bytes
import unittest
from Goap.Action import Actions

class ActionTest(unittest.TestCase):

    def setUp(self):
        self.actions = Actions()

    def test_add_action_success(self):
        self.actions.add(name='CreateVPC',
          pre_conditions={'vpc':False, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':False,  'app':False},
          shell='awscli vpc create')
        self.actions.add(name='CreateDB',
          pre_conditions={'vpc':True, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':True,  'app':False},
          shell='awscli vpc create')
        assert 'CreateVPC' == str(self.actions.get(name='CreateVPC'))
        assert 'CreateDB' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_success(self):
        self.actions.add(name='CreateVPC',
          pre_conditions={'vpc':False, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':False,  'app':False},
          shell='awscli vpc create')
        self.actions.add(name='CreateDB',
          pre_conditions={'vpc':True, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':True,  'app':False},
          shell='awscli vpc create')
        self.actions.remove(name='CreateVPC')
        assert 'CreateDB' == str(self.actions.get(name='CreateDB'))

    def test_remove_action_error(self):
        self.actions.add(name='CreateVPC',
          pre_conditions={'vpc':False, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':False,  'app':False},
          shell='awscli vpc create')
        self.actions.add(name='CreateDB',
          pre_conditions={'vpc':True, 
         'db':False,  'app':False},
          effects={'vpc':True, 
         'db':True,  'app':False},
          shell='awscli vpc create')
        self.actions.remove(name='CreateAPP')
        assert 'None' == str(self.actions.get(name='CreateAPP'))