# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils/test_timestamp.py
# Compiled at: 2017-03-02 16:31:16
# Size of source mod 2**32: 298 bytes
import datetime
from baroque.utils import timestamp

def test_utc_now():
    utc_ts = timestamp.utc_now()
    assert utc_ts.tzinfo is not None


def test_stringify():
    dateobj = datetime.datetime(1983, 7, 3, 9, 0, 0)
    result = timestamp.stringify(dateobj)
    assert isinstance(result, str)