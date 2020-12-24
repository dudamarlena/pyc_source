# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_tuned.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.tuned import Tuned
from insights.tests import context_wrap
TUNED_OUTPUT = ('\nAvailable profiles:\n- balanced\n- desktop\n- latency-performance\n- network-latency\n- network-throughput\n- powersave\n- throughput-performance\n- virtual-guest\n- virtual-host\nCurrent active profile: virtual-guest\n').strip()
TUNED_OUTPUT2 = ('\nAvailable profiles:\n- balanced\n- desktop\n- latency-performance\n- network-latency\n- network-throughput\n- powersave\n- throughput-performance\n- virtual-guest\n- virtual-host\nIt seems that tuned daemon is not running, preset profile is not activated.\nPreset profile: virtual-guest\n').strip()

def test_active_profile():
    tuned_output = Tuned(context_wrap(TUNED_OUTPUT))
    assert len(tuned_output.data.get('available')) == 9
    assert tuned_output.data.get('active') == 'virtual-guest'
    assert tuned_output.data.get('available') == ['balanced',
     'desktop',
     'latency-performance',
     'network-latency',
     'network-throughput',
     'powersave',
     'throughput-performance',
     'virtual-guest',
     'virtual-host']


def test_preset_profile():
    tuned_output = Tuned(context_wrap(TUNED_OUTPUT2))
    assert len(tuned_output.data.get('available')) == 9
    assert tuned_output.data.get('preset') == 'virtual-guest'
    assert tuned_output.data.get('available') == ['balanced',
     'desktop',
     'latency-performance',
     'network-latency',
     'network-throughput',
     'powersave',
     'throughput-performance',
     'virtual-guest',
     'virtual-host']