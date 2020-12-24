# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/test/test_errors.py
# Compiled at: 2009-05-01 11:44:33
"""
Tests for biblio.webquery.errors, using nose.
"""
import time
from biblio.webquery import errors

def test_querythrottleerror():
    err = errors.QueryThrottleError('my msg')
    assert str(err) == 'my msg'
    try:
        raise err
    except errors.QueryThrottleError, ex:
        assert str(err) == 'my msg'
    except:
        assert False, 'error should be caught elsewhere'