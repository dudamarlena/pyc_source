# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_environment.py
# Compiled at: 2016-03-16 03:48:56
# Size of source mod 2**32: 2733 bytes
from unittest import TestCase
from mad.environment import Environment

class EnvironmentTest(TestCase):

    def verify_binding(self, env, symbol, value):
        self.assertEqual(env.look_up(symbol), value)

    def verify_all_bindings(self, env, bindings):
        for symbol, value in bindings.items():
            self.verify_binding(env, symbol, value)

    def test_define_all_symbols(self):
        env = Environment()
        env.define_each(['a', 'b', 'c'], [1, 2, 3])
        self.verify_all_bindings(env, {'a': 1,  'b': 2,  'c': 3})

    def test_define_all_reject_missing_values(self):
        env = Environment()
        with self.assertRaises(ValueError):
            env.define_each(['a', 'b', 'c'], [1, 2])

    def test_look_up_bindings_in_parent(self):
        env1 = Environment()
        env1.define('my_var', 4)
        env2 = env1.create_local_environment()
        env3 = env2.create_local_environment()
        self.assertEqual(env3.look_up('my_var'), 4)

    def test_look_up_a_missing_binding(self):
        env1 = Environment()
        env1.define('var1', 5)
        self.assertIsNone(env1.look_up('missing_symbol'))

    def test_look_up_masked_bindings(self):
        env1 = Environment()
        env1.define('my_var', 8)
        env2 = env1.create_local_environment()
        env2.define('my_var', 7)
        env3 = env2.create_local_environment()
        env3.define('my_var', 6)
        self.assertEqual(env1.look_up('my_var'), 8)
        self.assertEqual(env2.look_up('my_var'), 7)
        self.assertEqual(env3.look_up('my_var'), 6)

    def test_dynamic_scope(self):
        env = Environment()
        local_env1 = env.create_local_environment()
        local_env1.define('var_1', 123)
        local_env2 = env.create_local_environment(local_env1)
        self.assertIsNone(local_env2.look_up('var_1'))
        self.assertEqual(local_env2.dynamic_look_up('var_1'), 123)