# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/projects/firelet/test/testingutils.py
# Compiled at: 2011-05-29 07:22:19
import logging, inspect, glob
from os import listdir, mkdir
from json import dumps
import shutil
from tempfile import mkdtemp
from time import time
USE_SHM = True
repodir = None

def setup_dir():
    global repodir
    if repodir:
        teardown_dir()
    if USE_SHM:
        tstamp = str(time())[5:]
        repodir = '/dev/shm/fl_%s' % tstamp
        mkdir(repodir)
    else:
        repodir = mkdtemp(prefix='tmp_fltest')
    globs = [
     'test/iptables-save*', 'test/ip-addr-show*', 'test/*.csv', 'test/*.json']
    for g in globs:
        for f in glob.glob(g):
            shutil.copy(f, repodir)

    li = listdir(repodir)
    assert len(li) > 5, 'Not enough file copied'


def teardown_dir():
    global repodir
    if repodir:
        shutil.rmtree(repodir)
        repodir = None
    return


def show(s, o=None):
    """Log an object representation"""
    stack = [ x[3] for x in inspect.stack() ]
    if 'runTest' in stack:
        rt = stack.index('runTest')
        stack = stack[1:rt]
    else:
        stack = stack[1:3]
    stack = ('->').join(reversed(stack))
    try:
        d = dumps(o, indent=2)
    except:
        d = repr(o)

    li = d.split('\n')
    if len(li) < 3:
        if o:
            return '%s %s: %s' % (stack, s, repr(o))
        else:
            return '%s %s' % (stack, s)

    else:
        indented = ('\n    ').join(li)
        return '\n-------- [%s] ---------\n    %s\n----- [end of %s] -----\n' % (s, indented, s)


def string_in_list(s, li):
    """Count how many times a string is contained in a list of strings
    No exact match is required
    >>> strings_in_list('p', ['apple'])
    1
    """
    return sum(1 for x in li if s in str(x))


def test_string_in_list():
    li = [
     'apple', 'p', '', None, 123, '   ']
    assert string_in_list('p', li) == 2
    return


def assert_equal_line_by_line(li1, li2):
    for x, y in zip(li1, li2):
        assert x == y, "'%s' differs from '%s' in:\n%s\n%s\n" % (repr(li1), repr(li2))


def duplicates(li):
    """Find duplicate elements in a list
    Return [ (item, number_of_instances), ... ]
    """
    return [ (i, li.count(i)) for i in set(li) if li.count(i) > 1 ]