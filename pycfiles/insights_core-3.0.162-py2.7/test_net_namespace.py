# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_net_namespace.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import net_namespace
from insights.parsers.net_namespace import NetworkNamespace
from insights.tests import context_wrap
from insights.parsers import SkipException
import pytest
LIST_NAMESPACE = ('\ntemp_netns  temp_netns_2  temp_netns_3\n').strip()
LIST_NAMESPACE_2 = ('\ntemp_netns\n').strip()
LIST_NAMESPACE_3 = ('\n').strip()
CMD_LIST_NAMESPACE = ('\ntemp_netns_3\ntemp_netns_2\ntemp_netns\n').strip()
CMD_LIST_NAMESPACE_2 = ('\ntemp_netns_3\n').strip()
CMD_LIST_NAMESPACE_3 = ('\n').strip()

def test_netstat_doc_examples():
    env = {'netns_obj': NetworkNamespace(context_wrap(LIST_NAMESPACE))}
    failed, total = doctest.testmod(net_namespace, globs=env)
    assert failed == 0


def test_bond_class():
    netns_obj = NetworkNamespace(context_wrap(LIST_NAMESPACE))
    assert netns_obj.netns_list.sort() == ['temp_netns', 'temp_netns_2', 'temp_netns_3'].sort()
    assert len(netns_obj.netns_list) == 3
    netns_obj = NetworkNamespace(context_wrap(LIST_NAMESPACE_2))
    assert netns_obj.netns_list == ['temp_netns']
    assert len(netns_obj.netns_list) == 1
    netns_obj = NetworkNamespace(context_wrap(CMD_LIST_NAMESPACE))
    assert netns_obj.netns_list.sort() == ['temp_netns', 'temp_netns_2', 'temp_netns_3'].sort()
    assert len(netns_obj.netns_list) == 3
    netns_obj = NetworkNamespace(context_wrap(CMD_LIST_NAMESPACE_2))
    assert netns_obj.netns_list == ['temp_netns_3']
    assert len(netns_obj.netns_list) == 1


def test_abnormal():
    with pytest.raises(SkipException) as (pe):
        NetworkNamespace(context_wrap(LIST_NAMESPACE_3))
    assert 'Nothing to parse.' in str(pe)
    with pytest.raises(SkipException) as (pe):
        NetworkNamespace(context_wrap(CMD_LIST_NAMESPACE_3))
    assert 'Nothing to parse.' in str(pe)