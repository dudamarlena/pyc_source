# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_getconf_pagesize.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers.getconf_pagesize import GetconfPageSize
from insights.tests import context_wrap
from insights.parsers import getconf_pagesize
import doctest
GETCONFPAGESIZE1 = ('\n4096\n').strip()
GETCONFPAGESIZE2 = ('\n16384\n').strip()

def test_getconf_PAGESIZE1():
    result = GetconfPageSize(context_wrap(GETCONFPAGESIZE1))
    assert result.page_size == 4096


def test_getconf_PAGESIZE2():
    result = GetconfPageSize(context_wrap(GETCONFPAGESIZE2))
    assert result.page_size == 16384


def test_doc():
    env = {'pagesize_parsed': GetconfPageSize(context_wrap(GETCONFPAGESIZE1))}
    print env
    failed, total = doctest.testmod(getconf_pagesize, globs=env)
    assert failed == 0