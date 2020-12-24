# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_dr_enabled.py
# Compiled at: 2019-05-16 13:41:33
from insights import combiner, dr
from insights.parsers.uname import Uname

def teardown_function(*args):
    for k in dr.ENABLED:
        dr.ENABLED[k] = True


@combiner()
def one():
    return 1


def test_enabled_string():
    assert dr.is_enabled('insights.core.context.HostContext')


def test_enabled_object():
    assert dr.is_enabled(Uname)


def test_disabled_string():
    dr.set_enabled('insights.core.context.HostContext', False)
    from insights.core.context import HostContext
    assert not dr.is_enabled(HostContext)


def test_disabled_object():
    dr.set_enabled(Uname, False)
    assert not dr.is_enabled(Uname)


def test_disabled_run():
    assert dr.ENABLED[one]
    broker = dr.run(dr.COMPONENTS[dr.GROUPS.single])
    assert one in broker
    dr.set_enabled(one, False)
    assert not dr.ENABLED[one]
    broker = dr.run(dr.COMPONENTS[dr.GROUPS.single])
    assert one not in broker