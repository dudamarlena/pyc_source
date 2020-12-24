# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/lib/core/network.py
# Compiled at: 2013-01-26 13:25:47
"""The network core submodule provide a useful way to manage network
interfaces in remote machine."""
import os, mico
from fabric.api import hide
from fabric.api import settings

def network_interfaces():
    """Return a list of available network interfaces in the remote host."""
    with settings(hide('running', 'stdout')):
        res = mico.run('/sbin/ifconfig -s')
        return map(lambda line: line.split(' ')[0], res.splitlines()[1:])


def network_address(iface=''):
    """Return a list of IP addresses associated with an specific interface
    or, if not provided, the full list of the system."""
    with settings(hide('running', 'stdout')):
        res = mico.run("/sbin/ifconfig %s | grep 'inet addr'" % iface)
        return map(lambda x: x.split()[1].split(':')[1], res.splitlines())


def network_netmask(iface=''):
    """Return a list of IP netmask associated with an specific interface
    or, if not provided, the full list of the system."""
    with settings(hide('running', 'stdout')):
        res = mico.run("/sbin/ifconfig %s | grep 'inet addr'" % iface)
        ret = []
        for _res in res.splitlines():
            field = _res.split()[2]
            if field.startswith('Mask'):
                ret.append(field.split(':')[1])
            else:
                field = res.split()[3]
                ret.append(field.split(':')[1])

        return ret


def network_nameservers():
    """Return a list with the nameservers present in the remote system."""
    with settings(hide('running', 'stdout')):
        res = mico.run('grep ^nameserver /etc/resolv.conf')
        return map(lambda x: x.split()[1], res.splitlines())