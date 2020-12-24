# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/aliases_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 3145 bytes
import unittest, test.bibliopixel.patch
from bibliopixel.project import aliases, importer
from bibliopixel.util import log
NOT_ANIMATIONS = [
 'bpa']

def patch(**kwds):
    return test.bibliopixel.patch.patch(aliases, 'PROJECT_ALIASES', kwds)


class AliasTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(aliases.resolve(''), '')

    def test_resolve(self):
        self.assertEqual(aliases.resolve('serial'), 'bibliopixel.drivers.serial.Serial')
        self.assertEqual(aliases.resolve('foo'), 'foo')
        with patch(foo='bar'):
            self.assertEqual(aliases.resolve('foo'), 'bar')
            self.assertEqual(aliases.resolve('@foo.bing'), 'bar.bing')
            self.assertEqual(aliases.resolve('$foo.bing'), 'bar.bing')
            self.assertEqual(aliases.resolve('bar.bing.@foo'), 'bar.bing.bar')
            self.assertEqual(aliases.resolve('bar.bing.$foo'), 'bar.bing.bar')
            self.assertEqual(aliases.resolve('x@foo'), 'x@foo')
            self.assertEqual(aliases.resolve('x$foo'), 'x$foo')

    def test_preserve_separators(self):
        s = '.asdfa./#fahdwrdr./#435'
        self.assertEqual(aliases.resolve(s), s)

    def test_marker(self):
        with patch(foo='bar.com/a.html'):
            result = aliases.resolve('https://@foo#tag')
        self.assertEqual(result, 'https://bar.com/a.html#tag')

    def test_marker_dollar(self):
        with patch(foo='bar.com/a.html'):
            result = aliases.resolve('https://$foo#tag')
        self.assertEqual(result, 'https://bar.com/a.html#tag')

    def test_existence(self):
        failed = []
        for name, cl in aliases.BUILTIN_ALIASES.items():
            try:
                importer.import_symbol(cl)
            except:
                failed.append(name)

        if failed != NOT_ANIMATIONS:
            (log.printer)('Failed', *failed, **{'sep': '\n'})
            self.assertTrue(False)

    def test_additional_aliases(self):
        additional = {'foo':'bar',  'remote':'distance'}
        self.assertEqual(aliases.resolve('foo', additional), 'bar')
        self.assertEqual(aliases.resolve('remote', additional), 'distance')

    def test_not_needed(self):
        just_one = ''
        failed, not_equal = [], []
        for alias, path in aliases.BUILTIN_ALIASES.items():
            if not alias in NOT_ANIMATIONS:
                if just_one:
                    if alias != just_one:
                        continue
                python_path = '.'.join(path.split('.', 2)[:2])
                expected = importer.import_symbol(path)
                try:
                    actual = importer.import_symbol(alias, python_path=python_path)
                except:
                    failed.append(alias)
                    if just_one:
                        raise

                if actual is not expected:
                    not_equal.append(alias)

        self.assertEqual([sorted(failed), sorted(not_equal)], [
         sorted(FAILED), sorted(NOT_EQUAL)])


FAILED = ('apa102', 'lpd8806', 'pi_ws281x', 'sk9822', 'spi', 'ws2801', 'ws281x')
NOT_EQUAL = ('serial', )