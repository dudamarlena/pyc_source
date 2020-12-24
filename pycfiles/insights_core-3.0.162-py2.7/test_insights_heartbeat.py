# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_insights_heartbeat.py
# Compiled at: 2019-05-16 13:41:33
from insights.core.plugins import make_fail
from insights.plugins import insights_heartbeat
from insights.parsers.hostname import Hostname
from insights.specs import Specs
from insights.tests import context_wrap, InputData, run_test
NON_MATCHING_HOSTNAME = 'some-other-hostname-that-doesnt-match'
good = Hostname(context_wrap(insights_heartbeat.HOST))
bad = Hostname(context_wrap(NON_MATCHING_HOSTNAME))

def test_heartbeat():
    expected_result = make_fail(insights_heartbeat.ERROR_KEY)
    assert expected_result == insights_heartbeat.is_insights_heartbeat(good)
    assert insights_heartbeat.is_insights_heartbeat(bad) is None
    return


def test_integration_tests():
    comp = insights_heartbeat.is_insights_heartbeat
    input_data = InputData(name='Match: no kernel')
    input_data.add(Specs.hostname, insights_heartbeat.HOST)
    expected = make_fail(insights_heartbeat.ERROR_KEY)
    run_test(comp, input_data, expected)
    input_data = InputData(name='No Match: bad hostname')
    input_data.add(Specs.hostname, NON_MATCHING_HOSTNAME)
    run_test(comp, input_data, None)
    return