# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_networkmanager_dhclient.py
# Compiled at: 2020-04-16 14:56:28
import doctest, pytest
from insights.parsers import networkmanager_dhclient, SkipException
from insights.parsers.networkmanager_dhclient import NetworkManagerDhclient
from insights.tests import context_wrap
DHCLIENT_RHEL_6 = '/etc/NetworkManager/dispatcher.d/10-dhclient'
DHCLIENT_RHEL_7 = '/etc/NetworkManager/dispatcher.d/11-dhclient'
NOT_VULNERABLE_RHEL_6 = ('\n#!/bin/bash\n# run dhclient.d scripts in an emulated environment\n\nPATH=/bin:/usr/bin:/sbin\nSAVEDIR=/var/lib/dhclient\nETCDIR=/etc/dhcp\ninterface=$1\n\neval "$(\ndeclare | LC_ALL=C grep \'^DHCP4_[A-Z_]*=\' | while read -r opt; do\n    optname=${opt%%=*}\n    optname=${optname,,}\n    optname=new_${optname#dhcp4_}\n    optvalue=${opt#*=}\n    echo "$optname=$optvalue"\ndone\n)"\n\n[ -f /etc/sysconfig/network ] && . /etc/sysconfig/network\n\n[ -f /etc/sysconfig/network-scripts/ifcfg-$interface ] &&     . /etc/sysconfig/network-scripts/ifcfg-$interface\n\nif [ -d $ETCDIR/dhclient.d ]; then\n    for f in $ETCDIR/dhclient.d/*.sh; do\n        if [ -x $f ]; then\n            subsystem="${f%.sh}"\n            subsystem="${subsystem##*/}"\n            . ${f}\n            if [ "$2" = "up" ]; then\n                "${subsystem}_config"\n            elif [ "$2" = "down" ]; then\n                "${subsystem}_restore"\n            fi\n        fi\n    done\nfi\n').strip()
VULNERABLE_RHEL_7 = ('\n#!/bin/bash\n# run dhclient.d scripts in an emulated environment\n\nPATH=/bin:/usr/bin:/sbin\nSAVEDIR=/var/lib/dhclient\nETCDIR=/etc/dhcp\ninterface=$1\n\neval "$(\ndeclare | LC_ALL=C grep \'^DHCP4_[A-Z_]*=\' | while read opt; do\n    optname=${opt%%=*}\n    optname=${optname,,}\n    optname=new_${optname#dhcp4_}\n    optvalue=${opt#*=}\n    echo "export $optname=$optvalue"\ndone\n)"\n\n[ -f /etc/sysconfig/network ] && . /etc/sysconfig/network\n\n[ -f /etc/sysconfig/network-scripts/ifcfg-$interface ] &&     . /etc/sysconfig/network-scripts/ifcfg-$interface\n\nif [ -d $ETCDIR/dhclient.d ]; then\n    for f in $ETCDIR/dhclient.d/*.sh; do\n        if [ -x $f ]; then\n            subsystem="${f%.sh}"\n            subsystem="${subsystem##*/}"\n            . ${f}\n            if [ "$2" = "up" ]; then\n                "${subsystem}_config"\n            elif [ "$2" = "dhcp4-change" ]; then\n                if [ "$subsystem" = "chrony" -o "$subsystem" = "ntp" ]; then\n                    "${subsystem}_config"\n                fi\n            elif [ "$2" = "down" ]; then\n                "${subsystem}_restore"\n            fi\n        fi\n    done\nfi\n').strip()

def test_no_data():
    with pytest.raises(SkipException):
        NetworkManagerDhclient(context_wrap(''))


def test_dhclient():
    dhclient_1 = NetworkManagerDhclient(context_wrap(VULNERABLE_RHEL_7, path=DHCLIENT_RHEL_7))
    assert dhclient_1.has_vulnerable_block
    dhclient_2 = NetworkManagerDhclient(context_wrap(NOT_VULNERABLE_RHEL_6, path=DHCLIENT_RHEL_6))
    assert not dhclient_2.has_vulnerable_block


def test_doc_examples():
    env = {'dhclient': NetworkManagerDhclient(context_wrap(VULNERABLE_RHEL_7, path=DHCLIENT_RHEL_7))}
    failed, total = doctest.testmod(networkmanager_dhclient, globs=env)
    assert failed == 0