# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/smoke_test.py
# Compiled at: 2016-10-26 07:59:49
import unittest
from lineprotocol import LineProtocolExporter

class SmokeTest(unittest.TestCase):

    def test(self):
        input = [
         [
          '1', 'foo', 'x', '24', '50.2', 'True'],
         [
          '2', 'bar', 'y', '25', '17.33', 'True'],
         [
          '3', 'baz', 'z', '26', '100', 'False']]
        exporter = LineProtocolExporter(labels=[
         'id', 'name', 'some_letter', 'some_number', 'percentage', 'status'], measurement='example', tag_columns=[
         'some_letter'], field_columns=[
         'id', 'name', 'percentage', 'status'], field_types=[
         'int', 'str', 'float', 'bool'], timestamp=1465839830100400200)
        output = ('\n').join([ exporter.export(line) for line in input ])
        expected_output = 'example,some_letter=x id=1i,name="foo",percentage=50.2,status=True 1465839830100400200\nexample,some_letter=y id=2i,name="bar",percentage=17.33,status=True 1465839830100400200\nexample,some_letter=z id=3i,name="baz",percentage=100,status=False 1465839830100400200'
        self.assertEqual(output, expected_output)