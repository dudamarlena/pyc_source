# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/importer_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2256 bytes
import unittest
from bibliopixel.project.importer import import_module, import_symbol, make_object
from bibliopixel.project import importer
from test.bibliopixel import patch

class ImporterTest(unittest.TestCase):

    def test_empty(self):
        import_symbol('')

    def test_single(self):
        import_module('math')
        import_module('bibliopixel')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            import_symbol('DOESNT_EXIST')

    def test_double(self):
        import_symbol('math.log')
        import_module('bibliopixel.util')

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            import_symbol('math12.log')
        with self.assertRaises(ImportError):
            import_symbol('math.log12')
        with self.assertRaises(ImportError):
            import_symbol('bibliopixel.log12')

    def test_longer(self):
        self.assertEqual(import_module('bibliopixel.project.importer'), importer)
        self.assertEqual(import_symbol('bibliopixel.project.importer.import_symbol'), import_symbol)

    def test_make_object(self):
        td = make_object(5, 23, typename='datetime.timedelta', milliseconds=35)
        import datetime
        self.assertEqual(td, datetime.timedelta(5, 23, milliseconds=35))

    def test_aliasing(self):
        import_symbol('bibliopixel.drivers.SimPixel.SimPixel')

    def test_exception_unknown(self):
        with self.assertRaises(ImportError) as (cm):
            import_symbol('nonexistent')
        e = str(cm.exception)
        self.assertFalse('pip install' in e)
        self.assertEqual("Cannot import symbol 'nonexistent'", e)

    def test_exception_known(self):
        names = dict((importer.INSTALL_NAMES), nonexistent='pynone')
        with patch.patch(importer, 'INSTALL_NAMES', names):
            importer.INSTALL_NAMES['nonexistent'] = 'pynone'
            with self.assertRaises(ImportError) as (cm):
                import_symbol('nonexistent')
            e = str(cm.exception)
            self.assertTrue('pip install pynone' in e)
            self.assertTrue("You are missing module 'nonexistent'" in e)