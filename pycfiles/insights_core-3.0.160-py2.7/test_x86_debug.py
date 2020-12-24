# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_x86_debug.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import SkipException
from insights.parsers import x86_debug
from insights.parsers.x86_debug import X86IBPBEnabled
from insights.parsers.x86_debug import X86PTIEnabled
from insights.parsers.x86_debug import X86IBRSEnabled
from insights.parsers.x86_debug import X86RETPEnabled
from insights.tests import context_wrap
import pytest, doctest

def test_x86_ibpb_enabled():
    ibpb = X86IBPBEnabled(context_wrap('0'))
    assert ibpb.value == 0
    assert isinstance(ibpb.value, int)
    ibpb = X86IBPBEnabled(context_wrap('1'))
    assert ibpb.value == 1
    assert isinstance(ibpb.value, int)
    ibpb = X86IBPBEnabled(context_wrap('2'))
    assert ibpb.value == 2
    assert isinstance(ibpb.value, int)


def test_x86_pti_enabled():
    pti = X86PTIEnabled(context_wrap('0'))
    assert pti.value == 0
    assert isinstance(pti.value, int)
    pti = X86PTIEnabled(context_wrap('1'))
    assert pti.value == 1
    assert isinstance(pti.value, int)


def test_x86_ibrs_enabled():
    ibrs = X86IBRSEnabled(context_wrap('0'))
    assert ibrs.value == 0
    assert isinstance(ibrs.value, int)
    ibrs = X86IBRSEnabled(context_wrap('1'))
    assert ibrs.value == 1
    assert isinstance(ibrs.value, int)
    ibrs = X86IBRSEnabled(context_wrap('2'))
    assert ibrs.value == 2
    assert isinstance(ibrs.value, int)


def test_x86_retp_enabled():
    retp = X86RETPEnabled(context_wrap('0'))
    assert retp.value == 0
    assert isinstance(retp.value, int)
    retp = X86RETPEnabled(context_wrap('1'))
    assert retp.value == 1
    assert isinstance(retp.value, int)
    retp = X86RETPEnabled(context_wrap('2'))
    assert retp.value == 2
    assert isinstance(retp.value, int)


def test_x86_enabled_documentation():
    """
    Here we test the examples in the documentation automatically using
    doctest.  We set up an environment which is similar to what a rule
    writer might see - a '/sys/kernel/debug/x86/*_enabled' output
    that has been passed in as a parameter to the rule declaration.
    """
    env = {'dva': X86IBPBEnabled(context_wrap('1')), 
       'dv': X86PTIEnabled(context_wrap('1')), 
       'dl': X86IBRSEnabled(context_wrap('1')), 
       'dval': X86RETPEnabled(context_wrap('1'))}
    failed, total = doctest.testmod(x86_debug, globs=env)
    assert failed == 0


def test_x86_ibpb_enabled_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        X86IBPBEnabled(context_wrap(''))
    assert 'Input content is empty' in str(sc1)


def test_x86_pti_enabled_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc2):
        X86PTIEnabled(context_wrap(''))
    assert 'Input content is empty' in str(sc2)


def test_x86_ibrs_enabled_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc3):
        X86IBRSEnabled(context_wrap(''))
    assert 'Input content is empty' in str(sc3)


def test_x86_retp_enabled_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc4):
        X86RETPEnabled(context_wrap(''))
    assert 'Input content is empty' in str(sc4)