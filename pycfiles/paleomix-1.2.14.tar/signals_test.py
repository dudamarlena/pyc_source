# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/signals_test.py
# Compiled at: 2019-10-27 09:55:00
import signal, paleomix.common.signals as signals, nose
from nose.tools import assert_equal

def test_signal__sigterm_to_str():
    assert_equal(signals.to_str(signal.SIGTERM), 'SIGTERM')


def test_signal__str_to_sigterm():
    assert_equal(signals.from_str('SIGTERM'), signal.SIGTERM)


@nose.tools.raises(KeyError)
def test_signal__to_str__unknown_signal():
    signals.to_str(1024)


@nose.tools.raises(KeyError)
def test_signal__from_str__unknown_signal():
    signals.from_str('SIGSMURF')


@nose.tools.raises(TypeError)
def test_signal__to_str__wrong_type():
    signals.to_str('SIGTERM')


@nose.tools.raises(TypeError)
def test_signal__from_str__wrong_type():
    signals.from_str(signal.SIGTERM)