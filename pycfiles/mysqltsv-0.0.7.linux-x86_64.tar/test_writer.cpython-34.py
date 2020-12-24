# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/tests/test_writer.py
# Compiled at: 2015-08-26 18:37:45
# Size of source mod 2**32: 857 bytes
import io
from nose.tools import eq_, raises
from ..writer import Writer

def test_writer():
    rows = [
     [
      'Foo', 5, None],
     [
      'Bar', 10, 'waffles']]
    expected = 'Thing\tAmount\tNotes\n' + 'Foo\t5\tNULL\n' + 'Bar\t10\twaffles\n'
    f = io.StringIO()
    writer = Writer(f, headers=['Thing', 'Amount', 'Notes'])
    for row in rows:
        writer.write(row)

    eq_(f.getvalue(), expected)


def test_none_string():
    rows = [
     [
      'Foo', 5, None],
     [
      'Bar', 10, 'waffles']]
    expected = 'Thing\tAmount\tNotes\n' + 'Foo\t5\t\\N\n' + 'Bar\t10\twaffles\n'
    f = io.StringIO()
    writer = Writer(f, headers=['Thing', 'Amount', 'Notes'], none_string='\\N')
    for row in rows:
        writer.write(row)

    eq_(f.getvalue(), expected)