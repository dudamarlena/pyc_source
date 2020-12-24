# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_brctl_show.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.brctl_show import BrctlShow
from insights.tests import context_wrap
from insights.parsers import brctl_show, ParseException
BRCTL_SHOW = ('\nbridge name     bridge id               STP enabled     interfaces\nbr0             8000.08002731ddfd       no              eth1\n                                                        eth2\n                                                        eth3\nbr1             8000.0800278cdb62       no              eth4\n                                                        eth5\nbr2             8000.0800278cdb63       yes             eth6\ndocker0         8000.0242d4cf2112       no\n').strip()
BRCTL_SHOW_TAB = '\nbridge name\tbridge id\t\tSTP enabled\tinterfaces\nbr0\t\t8000.2047478aa2e8\tno\t\tem1\n\t\t\t\t\t\t\tvnet0\n\t\t\t\t\t\t\tvnet1\nvirbr9\t\t8000.525400263a23\tyes\t\tvirbr9-nic\n'
BRCTL_SHOW_NO_BRIDGES = '\nbridge name     bridge id   STP enabled     interfaces\n\n'
BRCTL_SHOW_LESS_COLUMN = '\nbridge name     bridge id\n\n'
BRCTL_SHOW_ERROR = ('\n/usr/sbin/brctl: file not found\n').strip()
BRCTL_SHOW_TIMEOUT = ("\ntimeout: failed to run command `/usr/sbin/brctl':\n").strip()

def test_get_brctl_show():
    result1 = BrctlShow(context_wrap(BRCTL_SHOW_TAB)).group_by_iface
    assert result1['br0'] == {'bridge id': '8000.2047478aa2e8', 
       'STP enabled': 'no', 
       'interfaces': [
                    'em1', 'vnet0', 'vnet1']}
    result = BrctlShow(context_wrap(BRCTL_SHOW)).group_by_iface
    assert len(result) == 4
    assert result['br0'] == {'bridge id': '8000.08002731ddfd', 
       'STP enabled': 'no', 
       'interfaces': [
                    'eth1', 'eth2', 'eth3']}
    assert result['br1'] == {'bridge id': '8000.0800278cdb62', 
       'STP enabled': 'no', 
       'interfaces': [
                    'eth4', 'eth5']}
    assert result['br2'] == {'bridge id': '8000.0800278cdb63', 
       'STP enabled': 'yes', 
       'interfaces': [
                    'eth6']}
    assert result['docker0'] == {'bridge id': '8000.0242d4cf2112', 
       'STP enabled': 'no'}
    with pytest.raises(ParseException) as (e_info):
        brctl_show.BrctlShow(context_wrap(BRCTL_SHOW_ERROR))
    assert 'Invalid Data Found' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        brctl_show.BrctlShow(context_wrap(BRCTL_SHOW_LESS_COLUMN))
    assert 'Invalid Data Found' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        brctl_show.BrctlShow(context_wrap(BRCTL_SHOW_TIMEOUT))
    assert 'Invalid Data Found' in str(e_info.value)