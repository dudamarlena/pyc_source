# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/test_inject.py
# Compiled at: 2015-12-21 17:12:57
from unittest import TestCase
from pyage.core import inject
from pyage.core.inject import Inject, InjectWithDefault

class TestClass(object):

    @Inject('stats')
    @InjectWithDefault(('foo', 4))
    def __init__(self):
        super(TestClass, self).__init__()


class TestInject(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestInject, cls).setUpClass()
        inject.config = 'pyage.conf.test_conf'

    def test_inject(self):
        t = TestClass()
        self.assertTrue(hasattr(t, 'stats'))
        self.assertEqual(t.foo, 4)