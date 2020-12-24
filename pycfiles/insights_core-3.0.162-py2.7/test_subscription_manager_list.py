# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_subscription_manager_list.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from ...parsers import subscription_manager_list
from ...tests import context_wrap
subscription_manager_list_consumed_in_docs = '\n+-------------------------------------------+\n   Consumed Subscriptions\n+-------------------------------------------+\nSubscription Name: Red Hat Enterprise Linux Server, Premium (1-2 sockets) (Up to 1 guest)\nProvides:          Oracle Java (for RHEL Server)\n                   Red Hat Software Collections Beta (for RHEL Server)\n                   Red Hat Enterprise Linux Server\n                   Red Hat Beta\nSKU:               RH0155783S\nContract:          12345678\nAccount:           1000001\nSerial:            0102030405060708090\nPool ID:           8a85f981477e5284014783abaf5d4dcd\nActive:            True\nQuantity Used:     1\nService Level:     PREMIUM\nService Type:      L1-L3\nStatus Details:    Subscription is current\nSubscription Type: Standard\nStarts:            11/14/14\nEnds:              07/06/15\nSystem Type:       Physical\n'
subscription_manager_list_installed_in_docs = '\n+-------------------------------------------+\nInstalled Product Status\n+-------------------------------------------+\nProduct Name:   Red Hat Software Collections (for RHEL Server)\nProduct ID:     201\nVersion:        2\nArch:           x86_64\nStatus:         Subscribed\nStatus Details:\nStarts:         04/27/15\nEnds:           04/27/16\n\nProduct Name:   Red Hat Enterprise Linux Server\nProduct ID:     69\nVersion:        7.1\nArch:           x86_64\nStatus:         Subscribed\nStatus Details:\nStarts:         04/27/15\nEnds:           04/27/16\n'
subscription_manager_list_test_data = '\n+-------------------------------------------+\n   Consumed Subscriptions\n+-------------------------------------------+\nSubscription Name: Red Hat Enterprise Linux Server, Premium (1-2 sockets) (Up to 1 guest)\nSubscription Type: Standard\nStarts:            17/2\n'
subscription_manager_list_no_installed_products = '\nNo installed products to list\n'

def test_subscription_manager_list_exceptions():
    sml = subscription_manager_list.SubscriptionManagerListConsumed(context_wrap(subscription_manager_list_test_data))
    assert len(sml.records) == 1
    rec0 = sml.records[0]
    assert 'Subscription Name' in rec0
    assert 'Subscription Type' in rec0
    assert 'Starts' in rec0
    assert rec0['Starts'] == '17/2'
    assert 'Starts timestamp' not in rec0
    sml = subscription_manager_list.SubscriptionManagerListInstalled(context_wrap(subscription_manager_list_no_installed_products))
    assert sml.records == []


def test_subscription_manager_list_docs():
    env = {'installed': subscription_manager_list.SubscriptionManagerListInstalled(context_wrap(subscription_manager_list_installed_in_docs)), 
       'consumed': subscription_manager_list.SubscriptionManagerListConsumed(context_wrap(subscription_manager_list_consumed_in_docs))}
    failed, total = doctest.testmod(subscription_manager_list, globs=env)
    assert failed == 0