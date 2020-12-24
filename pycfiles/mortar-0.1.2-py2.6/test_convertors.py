# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/test_convertors.py
# Compiled at: 2008-12-19 12:41:15
import datetime, unittest
from fixtures import identity, check
from mortar import types
from mortar.interfaces import IFieldType, empty

class TestConvertors(unittest.TestCase):
    mapping = {types.datetime: [
                      (
                       '2008/02/01', datetime.datetime(2008, 2, 1, 0, 0)),
                      (
                       identity, TypeError('Could not adapt', identity, types.datetime)),
                      (
                       datetime.datetime(2008, 2, 1, 0, 0), identity),
                      (
                       'junk', TypeError('Could not adapt', 'junk', types.datetime))], 
       types.datetimes: [], types.date: [
                  (
                   '2008/02/01', datetime.date(2008, 2, 1)),
                  (
                   'junk', TypeError('Could not adapt', 'junk', types.date))], 
       types.dates: [], types.time: [], types.times: [], types.number: [
                    (
                     1.0, identity)], 
       types.numbers: [], types.text: [
                  ('some text', 'some text'),
                  (
                   'a unicode', identity),
                  (1, '1'),
                  (1.0, '1.0'),
                  (
                   datetime.datetime(2008, 1, 2, 0, 0), '2008/01/02 00:00:00'),
                  (
                   datetime.date(2008, 1, 2), '2008/01/02'),
                  (None, '')], 
       types.texts: [
                   (
                    datetime.datetime(2008, 1, 2, 0, 0), ('2008/01/02 00:00:00', )),
                   (
                    datetime.date(2008, 1, 2), ('2008/01/02', )),
                   (
                    [
                     datetime.datetime(2008, 1, 2, 0, 0)], ['2008/01/02 00:00:00']),
                   (
                    (
                     datetime.date(2008, 1, 2),), ['2008/01/02']),
                   (
                    'text', TypeError('Could not adapt', 'text', types.texts)),
                   (
                    'text', ('text', )),
                   (
                    1, ('1', )),
                   (
                    1.0, ('1.0', )),
                   (
                    None, [])], 
       types.reference: [], types.references: [], types.binary: [], types.binaries: []}

    def test_convertors(self):
        errors = []
        for (t, s2e) in self.mapping.items():
            for (s, e) in s2e:
                check(t, s, e, errors)

        if errors:
            self.fail('Conversion not as expected:\n' + ('\n').join(errors))


class TestConversion(unittest.TestCase):
    mapping = [
     ('some text', 'some text'),
     (
      'some text', identity),
     (
      1.0, identity),
     (
      [
       'some text'], ['some text']),
     (
      ('some text', ), ('some text', )),
     (
      (), empty), ([], empty),
     (
      [
       'some text'], identity),
     (
      ('some text', ), identity),
     (
      (1, 'x'), TypeError("Sequences must be of one type, could not convert 'x' to <InterfaceClass mortar.types.number>")),
     (
      [
       1, 'x'], TypeError("Sequences must be of one type, could not convert 'x' to <InterfaceClass mortar.types.number>")),
     (
      datetime.datetime(2008, 1, 2, 0, 0), identity),
     (
      datetime.date(2008, 1, 2), identity),
     (
      [
       datetime.datetime(2008, 1, 2, 0, 0)], [datetime.datetime(2008, 1, 2, 0, 0)]),
     (
      (
       datetime.datetime(2008, 1, 2, 0, 0),), (datetime.datetime(2008, 1, 2, 0, 0),)),
     (
      [
       datetime.date(2008, 1, 2)], [datetime.date(2008, 1, 2)]),
     (
      (
       datetime.date(2008, 1, 2),), (datetime.date(2008, 1, 2),))]

    def test_conversion(self):
        errors = []
        for (s, e) in self.mapping:
            check(IFieldType, s, e, errors)

        if errors:
            self.fail('Conversion not as expected:\n' + ('\n').join(errors))


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(TestConvertors),
     unittest.makeSuite(TestConversion)))