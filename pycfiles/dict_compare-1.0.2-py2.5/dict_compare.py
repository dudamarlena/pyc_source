# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dict_compare.py
# Compiled at: 2009-01-10 16:15:39
"""
This module implements a structure comparer

>>> da  = {1:"a"}
>>> dict_compare(da,da)
True
>>> dab = {1:"a",2:"b"}
>>> dict_compare(da,dab)
False
>>> dict_compare(dab,da)
False
>>> da2  = {1:"A"}
>>> dict_compare(da,da2)
False

# Probando con datos con tuples []
>>> sr = SimpleReporter()
>>> db   = {1:['foo', 'bar']}
>>> dict_compare(db,db,sr)
True
>>> sr.get_errors()

>>> sr = SimpleReporter()
>>> db2  = {1:['bar', 'foo']}
>>> dict_compare(db,db2,sr)
False
>>> len(sr.get_errors())
60

>>> sr = SimpleReporter()
>>> dc   = ['a', {'foo': 'bar'}]
>>> dict_compare(dc,dc,sr)
True
>>> dc2  = ['b', {'foo': 'bar'}]
>>> dict_compare(dc,dc2,sr)
False
>>> len(sr.get_errors())
38

>>> sr  = SimpleReporter()
>>> dd  = ['a']
>>> dd2 = {'k': 'v'}
>>> dict_compare(dd,dd2,sr)
False
>>> len(sr.get_errors())
60

Here we generate use failIfDiff and assertNoDiff to generate common diff (unified format) output from two dictionaries.

>>> dc   = ['a', {'foo': 'bar'}]
>>> failIfDiff(dc, dc, sr)
True
>>> assertNoDiff(dc, dc, sr)
True
>>> sr = SimpleReporter()
>>> dc2  = ['a', {'foo': 'bar2'}]
>>> failIfDiff(dc, dc2, sr)
False
>>> len(sr.get_errors())
85
>>> assertNoDiff(dc, dc2, sr)
False
>>> len(sr.get_errors())
85

"""
import sys, os, difflib
from pprint import pformat

def listToDict(l):
    d = {}
    for (k, v) in enumerate(l):
        d[k] = v

    return d


def reportNotFoundKeysIn(d1, d2, label):
    if isinstance(d1, (list, tuple)):
        d1 = listToDict(d1)
        d2 = listToDict(d2)
    difference = dict([ (key, value) for (key, value) in d1.iteritems() if key not in d2 ])
    if difference:
        return label + str(difference) + os.linesep
    else:
        return ''


def structure_inspector(d_expected, d_received):
    msg = ''
    if type(d_expected) == type(d_received):
        msg += reportNotFoundKeysIn(d_expected, d_received, 'Not In Received: ')
        msg += reportNotFoundKeysIn(d_received, d_expected, 'Not In Expected: ')
        differentKeysLabelShown = False
        if isinstance(d_expected, (list, tuple)):
            d_expected = listToDict(d_expected)
            d_received = listToDict(d_received)
        for expected_key in d_expected.keys():
            if expected_key in d_received:
                if d_expected[expected_key] != d_received[expected_key]:
                    if not differentKeysLabelShown:
                        msg += 'Different values in' + os.linesep
                    msg += "'%s':  %s != %s " % (repr(expected_key),
                     repr(d_expected[expected_key]),
                     repr(d_received[expected_key])) + os.linesep

    else:
        msg += 'Not same type: ' + repr(d_expected) + repr(type(d_expected)) + ' != ' + repr(d_received) + repr(type(d_received))
    return msg


def diff_inspector(d_expected, d_received):
    if isinstance(d_expected, (tuple, list, dict)):
        d_expected = [ pformat(d) for d in d_expected ]
    else:
        d_expected = [
         pformat(d_expected)]
    if isinstance(d_received, (tuple, list, dict)):
        d_received = [ pformat(d) for d in d_received ]
    else:
        d_received = [
         pformat(d_received)]
    diff = difflib.unified_diff(d_expected, d_received, fromfile='expected', tofile='received')
    return ('').join([ d + '\n' for d in diff ])


def dict_compare(d_expected, d_received, reporter=None, inspector=structure_inspector):
    if cmp(d_expected, d_received) == 0:
        return True
    if reporter != None:
        msg = inspector(d_expected, d_received)
        reporter(msg)
    return False


def failIfDiff(d_expected, d_received, reporter=None):
    return dict_compare(d_expected, d_received, reporter=reporter, inspector=diff_inspector)


assertNoDiff = failIfDiff

class SimpleReporter(object):

    def __init__(self):
        self._msg = None
        return

    def __call__(self, msg):
        self._msg = msg

    def get_errors(self):
        return self._msg


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()