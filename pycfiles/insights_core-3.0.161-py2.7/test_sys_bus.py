# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sys_bus.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import sys_bus, ParseException
from insights.parsers.sys_bus import CdcWDM
from insights.tests import context_wrap
SYS_DEVICE_USAGE = ('\n1\n').strip()
SYS_DEVICE_USAGE_EMPTY = ('\n\n').strip()
SYS_DEVICE_USAGE_INVALID = ('\nnot valid content\n').strip()

def test_netstat_doc_examples():
    env = {'device_usage': CdcWDM(context_wrap(SYS_DEVICE_USAGE))}
    failed, total = doctest.testmod(sys_bus, globs=env)
    assert failed == 0


def test_bond_dynamic_lb_class():
    device_usage = CdcWDM(context_wrap(SYS_DEVICE_USAGE))
    assert device_usage.device_usage_cnt == 1
    assert device_usage.device_in_use is True


def test_class_exceptions():
    with pytest.raises(ParseException) as (exc):
        device_usage = CdcWDM(context_wrap(SYS_DEVICE_USAGE_EMPTY))
        assert device_usage is None
    assert 'Invalid Content!' in str(exc)
    with pytest.raises(ParseException) as (exc):
        device_usage = CdcWDM(context_wrap(SYS_DEVICE_USAGE_INVALID))
        assert device_usage is None
    assert 'Invalid Content!' in str(exc)
    return