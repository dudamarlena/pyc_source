# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sys_kernel.py
# Compiled at: 2020-03-26 13:06:46
import doctest, pytest
from insights.parsers import sys_kernel
from insights.parsers.sys_kernel import SchedRTRuntime, SchedFeatures
from insights.tests import context_wrap
from insights.core import ParseException
SYS_KERNEL_RUNTIME_CONTENT_1 = ('\n-1\n').strip()
SYS_KERNEL_RUNTIME_CONTENT_2 = ('\n950000\n').strip()
SYS_KERNEL_RUNTIME_CONTENT_3 = ('\n950000\n-1\n').strip()
SYS_KERNEL_RUNTIME_CONTENT_4 = ('\nsss1\n').strip()
SYS_KERNEL_FEATURES = ('\nGENTLE_FAIR_SLEEPERS START_DEBIT NO_NEXT_BUDDY LAST_BUDDY CACHE_HOT_BUDDY\n').strip()

def test_sys_runtime_docs():
    failed, total = doctest.testmod(sys_kernel, globs={'srt': SchedRTRuntime(context_wrap(SYS_KERNEL_RUNTIME_CONTENT_2)), 
       'sfs': SchedFeatures(context_wrap(SYS_KERNEL_FEATURES))})
    assert failed == 0


def test_sys_kernel_1():
    result = SchedRTRuntime(context_wrap(SYS_KERNEL_RUNTIME_CONTENT_1))
    assert result.runtime_us == -1


def test_exception():
    with pytest.raises(ParseException):
        SchedRTRuntime(context_wrap(SYS_KERNEL_RUNTIME_CONTENT_3))
    with pytest.raises(ParseException):
        SchedRTRuntime(context_wrap(SYS_KERNEL_RUNTIME_CONTENT_4))