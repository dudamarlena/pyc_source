# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/common.py
# Compiled at: 2008-12-19 12:41:15
import unittest
from mortar import types
from zope.interface.verify import verifyObject

class ContentTests(unittest.TestCase):

    def setUp(self):
        raise NotImplementedError

    def test_interface(self):
        from mortar.interfaces import IContent
        verifyObject(IContent, self.content)

    def test_names_empty(self):
        self.assertEqual(self.content.names, [])

    def test_names_sorting(self):
        self.content['2'] = 2
        self.content['1'] = 1
        self.content['3'] = 3
        self.assertEqual(self.content.names, ['1', '2', '3'])

    def test_set_with_empty(self):
        self.content['x'] = ()
        self.assertEqual(self.content['x'].get(), None)
        return

    def test_getas_after_empty_set(self):
        self.content['x'] = ()
        self.assertEqual(self.content['x'].get(type=types.text), '')

    def test_set(self):
        pass

    def test_get(self):
        pass

    def test_cast(self):
        pass

    def test_del(self):
        pass

    def test_delete(self):
        pass

    def test_delete_not_there(self):
        pass