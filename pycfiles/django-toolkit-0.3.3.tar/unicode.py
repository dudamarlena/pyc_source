# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/tests/csv/unicode.py
# Compiled at: 2015-06-23 01:13:43
from django.utils import unittest
from django_toolkit.csv.unicode import UnicodeWriter, UnicodeReader, CastingUnicodeWriter
from tempfile import NamedTemporaryFile

class UnicodeWriterTestCase(unittest.TestCase):

    def test_write(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = UnicodeWriter(f, lineterminator='\n')
        csv_writer.writerow(['NAME', 'AGE'])
        csv_writer.writerow(['foo', '12'])
        csv_writer.writerow(['bar', '16'])
        f.seek(0)
        actual = f.read()
        expected = 'NAME,AGE\nfoo,12\nbar,16\n'
        self.assertEqual(actual, expected)


class CastingUnicodeWriterTestCase(unittest.TestCase):

    def test_write(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = CastingUnicodeWriter(f, lineterminator='\n')
        csv_writer.writerow(['NAME', 'AGE', 'THINGS'])
        csv_writer.writerow(['foo', 12, 12.31])
        csv_writer.writerow(['bar', 16, 78.89])
        f.seek(0)
        actual = f.read()
        expected = 'NAME,AGE,THINGS\nfoo,12,12.31\nbar,16,78.89\n'
        self.assertEqual(actual, expected)


class UnicodeReaderWriterTestCase(unittest.TestCase):

    def test_read(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = UnicodeWriter(f, lineterminator='\n')
        expected = [['NAME', 'AGE'],
         [
          'foo', '12'],
         [
          'bar', '16']]
        csv_writer.writerows(expected)
        f.seek(0)
        csv_reader = UnicodeReader(f)
        actual = [ line for line in csv_reader ]
        self.assertEqual(actual, expected)