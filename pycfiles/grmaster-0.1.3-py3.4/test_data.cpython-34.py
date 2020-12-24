# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/data/tests/test_data.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 1458 bytes
"""Tests for standard test tables."""
from grmaster import data
import io

def test_openfile():
    """Test if wrong data folder."""
    with data.openfile('students.csv') as (table):
        assert isinstance(table, io.IOBase)


def test_readbytes():
    """Test readbytes function (by readlines method."""
    first = bytes(''.join(data.readlines('students.csv')), 'utf-8')
    second = data.readbytes('students.csv')
    assert first == second


def test_readlines():
    """Just test."""
    with data.openfile('students.csv') as (table):
        first = table.readlines()
    second = data.readlines('students.csv')
    assert first == second