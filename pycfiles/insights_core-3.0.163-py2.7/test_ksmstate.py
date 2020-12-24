# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ksmstate.py
# Compiled at: 2019-12-13 11:35:35
from insights.parsers import ksmstate, SkipException, ParseException
from insights.parsers.ksmstate import KSMState
from insights.tests import context_wrap
import pytest, doctest
KSMSTATE0 = '0'
KSMSTATE1 = '1'
KSMSTATE2 = '2'
KSMSTATE_ab0 = ''
KSMSTATE_ab1 = 'abc'
KSMSTATE_ab2 = '\nabc\n1\n'

def test_ksmstate():
    ksm = KSMState(context_wrap(KSMSTATE0))
    assert ksm.is_running is False
    assert ksm.value == '0'
    ksm = KSMState(context_wrap(KSMSTATE1))
    assert ksm.is_running is True
    assert ksm.value == '1'
    ksm = KSMState(context_wrap(KSMSTATE2))
    assert ksm.is_running is False
    assert ksm.value == '2'


def test_ksmstate_exp():
    with pytest.raises(SkipException):
        KSMState(context_wrap(KSMSTATE_ab0))
    with pytest.raises(ParseException):
        KSMState(context_wrap(KSMSTATE_ab1))
    with pytest.raises(ParseException):
        KSMState(context_wrap(KSMSTATE_ab2))


def test_ksmstate_doc():
    env = {'ksm': KSMState(context_wrap(KSMSTATE0))}
    failed, total = doctest.testmod(ksmstate, globs=env)
    assert failed == 0