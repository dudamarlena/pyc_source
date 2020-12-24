# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/networkmanager_dhclient.py
# Compiled at: 2020-04-16 14:56:28
"""
NetworkManagerDhclient - file ``/etc/NetworkManager/dispatcher.d/*-dhclient``
=============================================================================
"""
import re
from insights.core import Parser
from insights.core.plugins import parser
from insights.parsers import SkipException
from insights.specs import Specs
VULNERABLE_BLOCK_RHEL_6 = re.compile(re.escape(('\neval "$(\ndeclare | LC_ALL=C grep \'^DHCP4_[A-Z_]*=\' | while read opt; do\n    optname=${opt%%=*}\n    optname=${optname,,}\n    optname=new_${optname#dhcp4_}\n    optvalue=${opt#*=}\n    echo "$optname=$optvalue"\ndone\n)"\n').strip()))
VULNERABLE_BLOCK_RHEL_7 = re.compile(re.escape(('\neval "$(\ndeclare | LC_ALL=C grep \'^DHCP4_[A-Z_]*=\' | while read opt; do\n    optname=${opt%%=*}\n    optname=${optname,,}\n    optname=new_${optname#dhcp4_}\n    optvalue=${opt#*=}\n    echo "export $optname=$optvalue"\ndone\n)"\n').strip()))

@parser(Specs.networkmanager_dispatcher_d)
class NetworkManagerDhclient(Parser):
    """
    Class for parsing ``/etc/NetworkManager/dispatcher.d/*-dhclient`` file.

    Attributes:
        has_vulnerable_block (bool): True, if the vulnerable block is present, False otherwise.

    Raises:
        SkipException: When content is empty or cannot be parsed.

    Sample output of this command is::

        #!/bin/bash
        # run dhclient.d scripts in an emulated environment

        PATH=/bin:/usr/bin:/sbin
        SAVEDIR=/var/lib/dhclient
        ETCDIR=/etc/dhcp
        interface=$1

        eval "$(
        declare | LC_ALL=C grep '^DHCP4_[A-Z_]*=' | while read opt; do
            optname=${opt%%=*}
            optname=${optname,,}
            optname=new_${optname#dhcp4_}
            optvalue=${opt#*=}
            echo "export $optname=$optvalue"
        done
        )"

        [ -f /etc/sysconfig/network ] && . /etc/sysconfig/network

        [ -f /etc/sysconfig/network-scripts/ifcfg-$interface ] &&             . /etc/sysconfig/network-scripts/ifcfg-$interface

        if [ -d $ETCDIR/dhclient.d ]; then
            for f in $ETCDIR/dhclient.d/*.sh; do
                if [ -x $f ]; then
                    subsystem="${f%.sh}"
                    subsystem="${subsystem##*/}"
                    . ${f}
                    if [ "$2" = "up" ]; then
                        "${subsystem}_config"
                    elif [ "$2" = "dhcp4-change" ]; then
                        if [ "$subsystem" = "chrony" -o "$subsystem" = "ntp" ]; then
                            "${subsystem}_config"
                        fi
                    elif [ "$2" = "down" ]; then
                        "${subsystem}_restore"
                    fi
                fi
            done
        fi

    Examples:
        >>> type(dhclient)
        <class 'insights.parsers.networkmanager_dhclient.NetworkManagerDhclient'>
        >>> dhclient.has_vulnerable_block
        True
    """

    def parse_content(self, content):
        if not content:
            raise SkipException('No content.')
        result = ('\n').join(content)
        match_rhel_6 = VULNERABLE_BLOCK_RHEL_6.search(result)
        match_rhel_7 = VULNERABLE_BLOCK_RHEL_7.search(result)
        self.has_vulnerable_block = bool(match_rhel_7) or bool(match_rhel_6)