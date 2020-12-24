# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_current_clocksource.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.current_clocksource import CurrentClockSource
from insights.tests import context_wrap
CLKSRC = '\ntsc\n'

def test_get_current_clksr():
    clksrc = CurrentClockSource(context_wrap(CLKSRC))
    assert clksrc.data == 'tsc'
    assert clksrc.is_kvm is False
    assert clksrc.is_vmi_timer != clksrc.is_tsc