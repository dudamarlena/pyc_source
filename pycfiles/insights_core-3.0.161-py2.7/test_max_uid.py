# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_max_uid.py
# Compiled at: 2019-12-13 11:35:35
import doctest, pytest
from insights.parsers import max_uid, ParseException, SkipException
from insights.parsers.max_uid import MaxUID
from insights.tests import context_wrap

def test_max_uid():
    with pytest.raises(SkipException):
        MaxUID(context_wrap(''))
    with pytest.raises(ParseException):
        MaxUID(context_wrap('1a'))
    max_uid = MaxUID(context_wrap('65536'))
    assert max_uid is not None
    assert max_uid.value == 65536
    return


def test_doc_examples():
    env = {'max_uid': MaxUID(context_wrap('65534'))}
    failed, total = doctest.testmod(max_uid, globs=env)
    assert failed == 0