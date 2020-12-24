# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/convertish/tests/test_basic.py
# Compiled at: 2010-03-11 11:00:13
from cStringIO import StringIO
import unittest, schemaish, schemaish.type
from datetime import date, datetime, time
from convertish.convert import string_converter, datetuple_converter, ConvertError
from convertish.util import SimpleTZInfo

class TestConverters(unittest.TestCase):

    def test_integer_to_string_conversion(self):
        type = schemaish.Integer()
        value_expected = [
         (0, '0'),
         (1, '1'),
         (1, '1')]
        for (value, expected) in value_expected:
            actual = string_converter(type).from_type(value)
            self.assertEquals(actual, expected)

        value_expected = [
         ('0', 0),
         ('1', 1),
         ('20', 20)]
        for (value, expected) in value_expected:
            actual = string_converter(type).to_type(value)
            self.assertEquals(actual, expected)

    def test_date_string_conversion(self):
        type = schemaish.Date()
        value = date(1966, 12, 18)
        expected = '1966-12-18'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)
        self.assertRaises(ConvertError, string_converter(type).to_type, 'nonsense')
        self.assertRaises(ConvertError, string_converter(type).to_type, '1990-1-1andabit')

    def test_float_string_conversion(self):
        type = schemaish.Float()
        value = 1.28
        expected = '1.28'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_boolean_string_conversion(self):
        type = schemaish.Boolean()
        value = True
        expected = 'True'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)
        value = False
        expected = 'False'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_file_string_converstion(self):
        FileType = schemaish.type.File
        type = schemaish.File()
        self.assertRaises(ValueError, string_converter(type).from_type, FileType(None, None, None))
        self.assertTrue(string_converter(type).from_type(FileType(StringIO('foo'), None, None)) == 'foo')
        file = string_converter(type).to_type('foo')
        self.assertTrue(file.mimetype == 'text/plain')
        self.assertTrue(file.filename == 'content.txt')
        self.assertTrue(file.file.read() == 'foo')
        return

    def test_date_datetuple_conversion(self):
        type = schemaish.Date()
        value = date(1966, 12, 18)
        expected = (1966, 12, 18)
        actual = datetuple_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = datetuple_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_sequencestring_string_conversion(self):
        type = schemaish.Sequence(schemaish.Integer())
        value = [1, 2, 3, 4]
        expected = '1,2,3,4'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_sequenceboolean_string_conversion(self):
        type = schemaish.Sequence(schemaish.Boolean())
        value = [True, False, True, True]
        expected = 'True,False,True,True'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_sequencesequenceinteger_string_conversion(self):
        type = schemaish.Sequence(schemaish.Sequence(schemaish.Integer()))
        value = [[1, 2, 3], [4, 5, 6]]
        expected = '1,2,3\n4,5,6'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_sequencetupleintegerstring_string_conversion(self):
        type = schemaish.Sequence(schemaish.Tuple((schemaish.Integer(), schemaish.String())))
        value = [(1, '1'), (2, '2')]
        expected = '1,1\n2,2'
        actual = string_converter(type).from_type(value)
        self.assertEquals(actual, expected)
        value, expected = expected, value
        actual = string_converter(type).to_type(value)
        self.assertEquals(actual, expected)

    def test_tuple_unicode(self):
        schema = schemaish.Tuple([schemaish.String(), schemaish.String()])
        converter = string_converter(schema)
        self.assertEquals(converter.from_type((('£1').decode('utf-8'), 'foo')), ('£1,foo').decode('utf-8'))
        self.assertEquals(converter.to_type(('£1,foo').decode('utf-8')), (('£1').decode('utf-8'), 'foo'))

    def test_tuple_noneifying(self):
        schema = schemaish.Tuple([schemaish.Integer(), schemaish.String()])
        converter = string_converter(schema)
        self.assertEquals(converter.from_type((None, None)), ',')
        self.assertEquals(converter.from_type((None, '')), ',')
        self.assertEquals(converter.from_type((None, 'foo')), ',foo')
        self.assertEquals(converter.from_type((1, None)), '1,')
        self.assertEquals(converter.to_type(','), (None, None))
        self.assertEquals(converter.to_type(',foo'), (None, 'foo'))
        self.assertEquals(converter.to_type('1,'), (1, None))
        return

    def test_time_string_conversion(self):
        schema = schemaish.Time()
        converter = string_converter(schema)
        tz = SimpleTZInfo(90)
        tests = [(time(1), '01:00:00'),
         (
          time(1, 2), '01:02:00'),
         (
          time(1, 2, 3), '01:02:03'),
         (
          time(1, 2, 3, 4), '01:02:03.000004'),
         (
          time(1, 0, 0, 0, tz), '01:00:00+01:30'),
         (
          time(1, 2, 0, 0, tz), '01:02:00+01:30'),
         (
          time(1, 2, 3, 0, tz), '01:02:03+01:30'),
         (
          time(1, 2, 3, 4, tz), '01:02:03.000004+01:30')]
        for (t, s) in tests:
            self.assertEquals(converter.from_type(t), s)
            self.assertEquals(converter.to_type(s), t)

    def test_datetime_string_conversion(self):
        schema = schemaish.DateTime()
        converter = string_converter(schema)
        tz = SimpleTZInfo(90)
        tests = [(datetime(2001, 2, 3, 4, 5, 6), '2001-02-03T04:05:06'),
         (
          datetime(2001, 2, 3), '2001-02-03T00:00:00'),
         (
          datetime(2001, 2, 3, 4, 5, 6, 7), '2001-02-03T04:05:06.000007'),
         (
          datetime(2001, 2, 3, 4, 5, 6, tzinfo=tz), '2001-02-03T04:05:06+01:30')]
        for (t, s) in tests:
            self.assertEquals(converter.from_type(t), s)
            self.assertEquals(converter.to_type(s), t)


if __name__ == '__main__':
    unittest.main()