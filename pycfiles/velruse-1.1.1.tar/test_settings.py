# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/work/oss/velruse/tests/units/test_settings.py
# Compiled at: 2013-06-08 23:24:54
import unittest

class TestProviderSettings(unittest.TestCase):

    def _makeOne(self, settings, prefix):
        from velruse.settings import ProviderSettings
        return ProviderSettings(settings, prefix=prefix)

    def test_it(self):
        p = self._makeOne({'v.foo': 'bar'}, 'v.')
        p.update('foo')
        self.assertEqual(p.kwargs, {'foo': 'bar'})
        p.update('foo', dst='baz')
        self.assertEqual(p.kwargs, {'foo': 'bar', 'baz': 'bar'})
        self.assertRaises(KeyError, p.update, 'missing', required=True)
        p.update('missing')
        self.assertEqual(p.kwargs, {'foo': 'bar', 'baz': 'bar'})