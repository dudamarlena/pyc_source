# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_bond_dynamic_lb.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import ParseException, SkipException
from insights.parsers.bond_dynamic_lb import BondDynamicLB
from insights.parsers import bond_dynamic_lb
from insights.tests import context_wrap
CONTEXT_PATH = '/sys/class/net/bond0/bonding/tlb_dynamic_lb'
CONTEXT_PATH_1 = '/sys/class/net/bond1/bonding/tlb_dynamic_lb'
CONTEXT_PATH_2 = '/sys/class/net/bond2/bonding/tlb_dynamic_lb'
BOND_LD_BALANCE = ('\n0\n').strip()
BOND_LD_BALANCE_1 = ('\n1\n').strip()
BOND_LD_BALANCE_2 = ('\noff\n').strip()
BOND_LD_BALANCE_NO = ('\n\n').strip()

def test_netstat_doc_examples():
    env = {'tlb_bond': BondDynamicLB(context_wrap(BOND_LD_BALANCE_1, CONTEXT_PATH))}
    failed, total = doctest.testmod(bond_dynamic_lb, globs=env)
    assert failed == 0


def test_bond_dynamic_lb_class():
    tlb_bond = BondDynamicLB(context_wrap(BOND_LD_BALANCE, CONTEXT_PATH))
    assert tlb_bond.bond_name == 'bond0'
    assert tlb_bond.dynamic_lb_status == 0
    tlb_bond = BondDynamicLB(context_wrap(BOND_LD_BALANCE_1, CONTEXT_PATH_1))
    assert tlb_bond.bond_name == 'bond1'
    assert tlb_bond.dynamic_lb_status == 1
    with pytest.raises(ParseException) as (exc):
        bond_obj = BondDynamicLB(context_wrap(BOND_LD_BALANCE_2, CONTEXT_PATH))
        assert not bond_obj.bond_name
    assert 'Unrecognised Values' in str(exc)
    with pytest.raises(SkipException) as (exc):
        bond_obj = BondDynamicLB(context_wrap(BOND_LD_BALANCE_NO, CONTEXT_PATH))
        assert not bond_obj.bond_name
    assert 'No Contents' in str(exc)