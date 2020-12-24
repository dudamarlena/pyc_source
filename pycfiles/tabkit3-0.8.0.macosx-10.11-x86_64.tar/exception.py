# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tabkit/exception.py
# Compiled at: 2016-06-08 10:21:29
import sys, types
from functools import wraps

class TabkitException(Exception):
    pass


def handle_exceptions(f, stderr=None, script=None):
    stderr = stderr or sys.stderr
    script = script or sys.argv[0]
    try:
        return f()
    except TabkitException as e:
        print >> stderr, '%s: %s' % (script, e)


def decorate_exceptions(f):

    @wraps(f)
    def wrapper():
        return handle_exceptions(f)

    return wrapper


def test_exception(f):

    def wrapper():
        result = f()
        if isinstance(result, types.GeneratorType):
            return list(result)
        return result

    return handle_exceptions(wrapper, stderr=sys.stdout, script='doctest')