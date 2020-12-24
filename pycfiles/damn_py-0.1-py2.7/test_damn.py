# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/tests/test_damn.py
# Compiled at: 2015-10-17 21:07:43
import unittest2 as unittest, os
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
FIXT = lambda n: os.path.join(TEST_DIR, 'fixtures', n)

class DamnTest(unittest.TestCase):

    def test_basic_damn_yaml(self):
        import yaml, damn
        with open(FIXT('abc.yml'), 'r') as (fh):
            yml = fh.read()
        yaml_abc = yaml.load(yml)
        damn_abc = damn.load(FIXT('abc'))
        mom = {'hi': 'mom'}
        self.assertEqual(damn_abc, yaml_abc)
        self.assertEqual(damn.load(FIXT('dir/and/markup/nest')), mom)
        self.assertEqual(damn.load(FIXT('dir')), {'and': {'markup': {'nest': mom}}})
        self.assertEqual(damn.load(FIXT('foo')), {'bar': damn.load(FIXT('bar'))})
        self.assertEqual(damn.load(FIXT('foo/bar')), damn.load(FIXT('bar')))