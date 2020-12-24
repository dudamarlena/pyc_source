# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/test_field_types.py
# Compiled at: 2008-12-19 12:41:15
import unittest
from datetime import datetime, date, time
from mortar import types
from mortar.interfaces import empty
from fixtures import check

class TestType(unittest.TestCase):
    mapping = (
     (None, None),
     (
      (), IndexError('tuple index out of range')),
     (
      (None, ), KeyError(type(None))),
     (
      datetime(2008, 1, 1, 20, 0), types.datetime),
     (
      (
       datetime(2008, 1, 1, 20),), types.datetimes),
     (
      date(2008, 1, 1), types.date),
     (
      [
       date(2008, 1, 1)], types.dates),
     (
      time(20, 0), types.time),
     (
      [
       time(20, 0)], types.times),
     (
      0, types.number),
     (
      0.0, types.number),
     (
      [
       0], types.numbers),
     (
      [
       0.0], types.numbers),
     (
      [
       0, ''], types.numbers),
     (
      'text', types.text),
     (
      [
       'text'], types.texts),
     (
      'a string', types.binary),
     (
      [
       'a string'], types.binaries),
     (
      empty, None))

    def test_type(self):
        errors = []
        for (o, e) in self.mapping:
            check(types.type, o, e, errors)

        if errors:
            self.fail('Type mapping not as expected:\n' + ('\n').join(errors))


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(TestType),))