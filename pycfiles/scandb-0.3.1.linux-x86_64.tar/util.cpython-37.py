# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/util.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 2114 bytes
import hashlib
BUF_SIZE = 65536

def hash_file(filename):
    """
    Calculate a SHA-512 hash from the given file.
    :param filename: File from which the hash should be calculated
    :return:
    """
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as (f):
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)

    return sha512.hexdigest()


def get_open_ports(host, protocol='tcp'):
    ports = []
    for port, proto in host.get_open_ports():
        if protocol == proto:
            ports.append(port)

    return ports


def get_ports(host):
    """
    This function generates a list of open ports. Each entry is a tuple which contains the port, protocol, servicename,
    state and a banner string.

    :param host: The NmapHost object
    :type host libnmap.objects.host.NmapHost

    :return: list of tuples
    """
    ports = []
    for port, proto in host.get_ports():
        if host.get_service(port, proto) is not None:
            service = host.get_service(port, proto)
            servicename = service.service
            state = service.state
            banner = service.banner
            ports.append((port, proto, servicename, state, banner))

    return ports


def get_hostname(host):
    """
    This function get the hostname of the given host.

    :param host: The NmapHost object
    :type host: libnmap.objects.host.NmapHost

    :return: hostname
    :rtype: str
    """
    hostname = ''
    for name in host.hostnames:
        if name == 'localhost':
            if hostname != '':
                continue
        hostname = name

    return hostname


def get_best_os_match(host):
    os_matches = host.os_match_probabilities()
    os = ''
    os_gen = ''
    if len(os_matches) > 0:
        os = os_matches[0].name
        if len(os_matches[0].osclasses) > 0:
            os_gen = os_matches[0].osclasses[0].osgen
    return (
     os, os_gen)


def host_to_tupel(host):
    hostname = get_hostname(host)
    os, os_gen = get_best_os_match(host)
    return (host.address, hostname, os, os_gen, host.status)