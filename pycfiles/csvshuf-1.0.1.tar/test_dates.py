# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ae/bzr/csvsee/tests/test_dates.py
# Compiled at: 2010-09-14 13:08:49
__doc__ = 'Unit tests for the `csvsee.dates` module\n'
import os
from datetime import datetime
from csvsee import dates
from nose.tools import assert_raises
from . import write_tempfile

def test_guess_date_format():
    """Test the `dates.guess_date_format` function.
    """
    date_formats = [
     ('2010/01/28 12:34:56 PM', '%Y/%m/%d %I:%M:%S %p'),
     ('01/28/10 1:25:49 PM', '%m/%d/%y %I:%M:%S %p'),
     ('01/28/2010 13:25:49.123', '%m/%d/%Y %H:%M:%S.%f')]
    for (date, format) in date_formats:
        assert dates.guess_date_format(date) == format


def test_guess_file_date_format():
    """Test the `dates.guess_file_date_format` function.
    """
    data_formats = [
     ('2010/01/28 12:34:56 PM', '%Y/%m/%d %I:%M:%S %p'),
     ('01/28/10 1:25:49 PM', '%m/%d/%y %I:%M:%S %p'),
     ('01/28/2010 13:25:49.123', '%m/%d/%Y %H:%M:%S.%f'),
     ('2010/08/30 13:57:14 blah', '%Y/%m/%d %H:%M:%S'),
     ('8/30/2010 13:57 blah', '%m/%d/%Y %H:%M'),
     ('8/30/2010 1:57:00 PM blah', '%m/%d/%Y %I:%M:%S %p')]
    for (data, expected) in data_formats:
        filename = write_tempfile(data)
        try:
            try:
                actual = dates.guess_file_date_format(filename)
            except:
                assert False
            else:
                assert actual == expected

        finally:
            os.unlink(filename)


def test_guess_file_date_format_exception():
    filename = write_tempfile('Data file without a date')
    assert_raises(dates.CannotParseDate, dates.guess_file_date_format, filename)
    os.unlink(filename)