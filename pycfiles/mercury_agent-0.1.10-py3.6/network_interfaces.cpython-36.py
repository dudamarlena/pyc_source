# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/network_interfaces.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 3252 bytes
import netifaces

def get_default_interface():
    """Get default AF_INET interfaces.

    :return: kernel device name or '' if no default interface found.
    """
    gws = netifaces.gateways()
    if 'default' not in gws:
        return ''
    route = gws['default'].get(netifaces.AF_INET)
    if route:
        return route[1]


def get_link_addresses(exclude_loopback=True):
    """Format a list containing AF_LINK info for each interface.

    :param exclude_loopback: Bool
    :return: list of dicts : {
        'interface': interface_name,
        'mac_address': ethernet address
    }
    """
    interfaces = list_interfaces(exclude_loopback)
    link_info = []
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        link_address = addresses.get(netifaces.AF_LINK)
        if link_address:
            link_info.append({'interface':interface, 
             'mac_address':link_address[0]['addr']})

    return link_info


def get_ipv4_network_info(interface):
    """Helper to get only AF_INET addresses.

    Be aware this function will return a list of addresses associated
    with the interface. The order of the list is unknown and matching
    networks to routes may be required in instances where there are multiple
    addresses (vlans, aliases, etc). As such, our code should check the
    length of the list even when we assume a length of 1.

    :param interface: device name, eth0, enp3s0, em1, etc.
    :return: A list of ipv4 info dicts {addr, broadcast || peer, netmask}
    """
    if interface not in list_interfaces():
        return []
    else:
        addresses = netifaces.ifaddresses(interface)
        return addresses.get(netifaces.AF_INET, [])


def get_ipv6_network_info(interface):
    """The same as get_ipv4_network_info but for AF_INET6

    :param interface: device name, eth0, enp3s0, em1, etc.
    :return: A list of ipv6 info dicts {addr, broadcast || peer, netmask}
    """
    if interface not in list_interfaces():
        return []
    else:
        addresses = netifaces.ifaddresses(interface)
        return addresses.get(netifaces.AF_INET6, [])


def list_interfaces(exclude_loopback=True):
    """Helper function to get network interfaces.

    :param exclude_loopback: If True, then the loopback interface is not
        included in the returned list. If False, the loopback interface will
        be included.
    :return: A list of interfaces.
    """
    interfaces = netifaces.interfaces()
    if exclude_loopback:
        interfaces = [i for i in interfaces if i != 'lo']
    return interfaces