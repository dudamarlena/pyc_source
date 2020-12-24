# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/btrdb/utils/test_timez.py
# Compiled at: 2019-09-30 18:27:35
# Size of source mod 2**32: 6112 bytes
__doc__ = '\nTesting for the btrdb.timez module\n'
import pytz, pytest, datetime, numpy as np
from freezegun import freeze_time
from btrdb.utils.timez import currently_as_ns, datetime_to_ns, ns_to_datetime, to_nanoseconds, ns_delta

class TestCurrentlyAsNs(object):

    def test_currently_as_ns(self):
        """
        Assert currently_as_ns returns correct value
        """
        expected = 1514808000000000000
        with freeze_time('2018-01-01 12:00:00 -0000'):
            assert currently_as_ns() == expected


class TestDatetimeToNs(object):

    def test_datetime_to_ns_naive(self):
        """
        Assert datetime_to_ns handles naive datetime
        """
        dt = datetime.datetime(2018, 1, 1, 12)
        localized = pytz.utc.localize(dt)
        expected = int(localized.timestamp() * 1000000000.0)
        assert dt.tzinfo is None
        assert datetime_to_ns(dt) == expected

    def test_datetime_to_ns_aware(self):
        """
        Assert datetime_to_ns handles tz aware datetime
        """
        eastern = pytz.timezone('US/Eastern')
        dt = datetime.datetime(2018, 1, 1, 17, tzinfo=eastern)
        expected = int(dt.astimezone(pytz.utc).timestamp() * 1000000000.0)
        assert dt.tzinfo is not None
        assert datetime_to_ns(dt) == expected


class TestNsToDatetime(object):

    def test_ns_to_datetime_is_utc(self):
        """
        Assert ns_to_datetime returns UTC aware datetime
        """
        dt = datetime.datetime.utcnow()
        ns = int(dt.timestamp() * 1000000000.0)
        assert dt.tzinfo is None
        assert ns_to_datetime(ns).tzinfo == pytz.UTC

    def test_ns_to_datetime_is_correct(self):
        """
        Assert ns_to_datetime returns correct datetime
        """
        val = 1514808000000000000
        expected = datetime.datetime(2018, 1, 1, 12, tzinfo=(pytz.UTC))
        assert ns_to_datetime(val) == expected


class TestToNanoseconds(object):

    def test_datetime_to_ns_naive(self):
        """
        Assert to_nanoseconds handles naive datetime
        """
        dt = datetime.datetime(2018, 1, 1, 12)
        localized = pytz.utc.localize(dt)
        expected = int(localized.timestamp() * 1000000000.0)
        assert dt.tzinfo is None
        assert to_nanoseconds(dt) == expected

    def test_datetime_to_ns_aware(self):
        """
        Assert to_nanoseconds handles tz aware datetime
        """
        eastern = pytz.timezone('US/Eastern')
        dt = datetime.datetime(2018, 1, 1, 17, tzinfo=eastern)
        expected = int(dt.astimezone(pytz.utc).timestamp() * 1000000000.0)
        assert dt.tzinfo is not None
        assert to_nanoseconds(dt) == expected

    def test_str(self):
        """
        Assert to_nanoseconds handles RFC3339 format
        """
        dt = datetime.datetime(2018, 1, 1, 12, tzinfo=(pytz.utc))
        expected = int(dt.timestamp() * 1000000000.0)
        dt_str = '2018-1-1 12:00:00.0-0000'
        assert dt.tzinfo is not None
        assert to_nanoseconds(dt_str) == expected
        dt_str = '2018-1-1 7:00:00.0-0500'
        dt = datetime.datetime(2018, 1, 1, 12, tzinfo=(pytz.timezone('US/Eastern')))
        assert dt.tzinfo is not None
        assert to_nanoseconds(dt_str) == expected
        dt_str = '2018-01-15 07:32:49'
        dt = datetime.datetime(2018, 1, 15, 7, 32, 49, tzinfo=(pytz.utc))
        expected = int(dt.timestamp() * 1000000000.0)
        assert to_nanoseconds(dt_str) == expected

    def test_str_midnight(self):
        """
        Test parse a date at midnight
        """
        expected = datetime.datetime(2019, 4, 7, tzinfo=(pytz.utc))
        expected = int(expected.timestamp() * 1000000000.0)
        assert to_nanoseconds('2019-04-07') == expected

    def test_str_raise_valueerror--- This code section failed: ---

 L. 148         0  LOAD_STR                 '01 Jan 2018 12:00:00 -0000'
                2  STORE_FAST               'dt_str'

 L. 149         4  LOAD_GLOBAL              pytest
                6  LOAD_ATTR                raises
                8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'RFC3339'
               12  LOAD_CONST               ('match',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  SETUP_WITH           32  'to 32'
               18  STORE_FAST               'exc'

 L. 150        20  LOAD_GLOBAL              to_nanoseconds
               22  LOAD_FAST                'dt_str'
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH       16  '16'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30

    def test_int(self):
        """
        Assert to_nanoseconds handles int
        """
        assert 42 == to_nanoseconds(42)

    def test_float(self):
        """
        Assert to_nanoseconds handles float
        """
        assert 42 == to_nanoseconds(42.0)

    def test_float_raise_valueerror--- This code section failed: ---

 L. 168         0  LOAD_GLOBAL              pytest
                2  LOAD_METHOD              raises
                4  LOAD_GLOBAL              ValueError
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           24  'to 24'
               10  STORE_FAST               'exc'

 L. 169        12  LOAD_GLOBAL              to_nanoseconds
               14  LOAD_CONST               42.5
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  BEGIN_FINALLY    
             24_0  COME_FROM_WITH        8  '8'
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  END_FINALLY      

 L. 170        30  LOAD_STR                 'can only convert whole numbers'
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'exc'
               36  CALL_FUNCTION_1       1  ''
               38  COMPARE_OP               in
               40  POP_JUMP_IF_TRUE     46  'to 46'
               42  LOAD_ASSERT              AssertionError
               44  RAISE_VARARGS_1       1  ''
             46_0  COME_FROM            40  '40'

Parse error at or near `BEGIN_FINALLY' instruction at offset 22

    def test_float(self):
        """
        Assert to_nanoseconds handles float
        """
        dt = datetime.datetime(2018, 1, 1, 12, tzinfo=(pytz.utc))
        expected = int(dt.timestamp() * 1000000000.0)
        dt64 = np.datetime64('2018-01-01T12:00')
        assert expected == to_nanoseconds(dt64)


class TestToNsDelta(object):

    def test_ns_delta(self):
        """
        Assert ns_delta converts inputs properly
        """
        val = ns_delta(1, 2, 1, 3, 1, 23, 1)
        assert val == 93663001023001

    def test_ns_delta_precision(self):
        """
        Assert ns_delta deals with real inputs
        """
        val = ns_delta(days=365, minutes=0.5, nanoseconds=1)
        assert val == int(3.1536e+16) + int(30000000000.0) + 1

    def test_returns_int(self):
        """
        Assert ns_delta returns int if floats used for arguments
        """
        val = ns_delta(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1)
        assert val == int(90061001001001.0)
        assert isinstance(val, int)