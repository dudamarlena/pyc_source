# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ae/bzr/csvsee/tests/test_grinder.py
# Compiled at: 2010-09-14 13:09:08
"""Unit tests for the `csvsee.grinder` module.
"""
import os, sys
from csvsee import grinder
from nose.tools import assert_raises
from . import data_dir, temp_filename

def test_get_test_names():
    """Test the `get_test_names` function.
    """
    outfile = os.path.join(data_dir, 'out_XP-0.log')
    assert grinder.get_test_names(outfile) == {1001: 'First test', 
       1002: 'Second test', 
       1003: 'Third test', 
       1004: 'Fourth test', 
       1005: 'Fifth test', 
       1006: 'Sixth test'}


def test_Bin():
    """Test the `Bin` class.
    """
    bin = grinder.Bin(['Errors', 'Test time'])
    assert bin.count == 0
    assert bin.average('Errors') == 0


def test_Test():
    """Test the `Test` class.
    """
    tst = grinder.Test(101, 'Foobared', 30)
    assert tst.number == 101
    assert tst.name == 'Foobared'
    assert tst.resolution == 30
    assert tst.timestamp_range() == (0, 0)


def test_empty_Report():
    """Test the `Report` class with an out* file having no test names
    (that is, a file that's either not a Grinder out* file, or one that
    hasn't finished writing test names to the end).
    """
    outfile = os.path.join(data_dir, 'incomplete.log')
    assert_raises(grinder.NoTestNames, grinder.Report, 60, outfile)


def test_Report():
    """Test the `Report` class.
    """
    outfile = os.path.join(data_dir, 'out_XP-0.log')
    data0 = os.path.join(data_dir, 'data_XP-0.log')
    data1 = os.path.join(data_dir, 'data_XP-1.log')
    report = grinder.Report(60, outfile, data0, data1)
    assert report.resolution == 60
    test_timestamp_ranges = [
     (1001, 1283195400, 1283195760),
     (1002, 1283195400, 1283195760),
     (1003, 1283195400, 1283195760),
     (1004, 1283195400, 1283195760),
     (1005, 1283195460, 1283195820),
     (1006, 1283195460, 1283195820)]
    for (test_number, start, end) in test_timestamp_ranges:
        assert report.tests[test_number].timestamp_range() == (start, end)

    assert report.timestamp_range() == (1283195400, 1283195820)
    test = report.tests[1006]
    assert test.stat_at_time('Test time', 1283195460) == 2333
    assert test.stat_at_time('Test time', 1283195760) == 2411
    assert test.stat_at_time('Test time', 1283195820) == 2848
    assert test.stat_at_time('Errors', 1283195460) == 0
    assert test.stat_at_time('Errors', 1283195760) == 0
    assert test.stat_at_time('Errors', 1283195820) == 0
    assert test.stat_at_time('Test time', 9999999999) == 0
    assert test.stat_at_time('Errors', 9999999999) == 0
    assert_raises(ValueError, test.stat_at_time, 'Fake Stat', 1283195460)
    bin = test.bins[1283195460]
    assert bin.count == 12
    assert bin.stats == {'Errors': 0, 
       'HTTP response errors': 0, 
       'HTTP response length': 1956, 
       'Test time': 28006}
    assert bin.average('HTTP response length') == 163
    assert str(test) == '1006: Sixth test'
    report_csv = temp_filename('csv')
    report.write_csv('Test time', report_csv)
    lines = [ line.rstrip() for line in open(report_csv) ]
    assert lines == [
     'GMT,1001: First test,1002: Second test,1003: Third test,1004: Fourth test,1005: Fifth test,1006: Sixth test',
     '08/30/2010 19:10:00.000,1546,318,2557,35882,0,0',
     '08/30/2010 19:11:00.000,0,0,0,0,1883,2333',
     '08/30/2010 19:12:00.000,0,0,0,0,0,0',
     '08/30/2010 19:13:00.000,0,0,0,0,0,0',
     '08/30/2010 19:14:00.000,0,0,0,0,0,0',
     '08/30/2010 19:15:00.000,0,0,0,0,0,0',
     '08/30/2010 19:16:00.000,1270,322,2196,33988,2054,2411',
     '08/30/2010 19:17:00.000,0,0,0,0,2080,2848']
    os.unlink(report_csv)


def test_grinder_files():
    """Test the `grinder_files` function.
    """
    outfile = os.path.join(data_dir, 'out_XP-0.log')
    data0 = os.path.join(data_dir, 'data_XP-0.log')
    data1 = os.path.join(data_dir, 'data_XP-1.log')
    assert grinder.grinder_files(data_dir) == [
     (
      outfile, [data0, data1])]
    assert_raises(ValueError, grinder.grinder_files, 'f00b4r')