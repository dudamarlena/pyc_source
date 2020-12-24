# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/bus.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 1817 bytes
import os, re
_escape_pat = re.compile('%([0-9A-Fa-f]{2})')

def unescape(v):

    def repl(match):
        n = int((match.group(1)), base=16)
        return chr(n)

    return _escape_pat.sub(repl, v)


def parse_addresses(s):
    for addr in s.split(';'):
        transport, info = addr.split(':', 1)
        kv = {}
        for x in info.split(','):
            k, v = x.split('=', 1)
            kv[k] = unescape(v)

        yield (
         transport, kv)


SUPPORTED_TRANSPORTS = ('unix', )

def get_connectable_addresses(addr):
    unsupported_transports = set()
    found = False
    for transport, kv in parse_addresses(addr):
        if transport not in SUPPORTED_TRANSPORTS:
            unsupported_transports.add(transport)
        else:
            if transport == 'unix':
                if 'abstract' in kv:
                    yield '\x00' + kv['abstract']
                    found = True
                elif 'path' in kv:
                    yield kv['path']
                    found = True

    if not found:
        raise RuntimeError('DBus transports ({}) not supported. Supported: {}'.format(unsupported_transports, SUPPORTED_TRANSPORTS))


def find_session_bus():
    addr = os.environ['DBUS_SESSION_BUS_ADDRESS']
    return next(get_connectable_addresses(addr))


def find_system_bus():
    addr = os.environ.get('DBUS_SYSTEM_BUS_ADDRESS', '') or 'unix:path=/var/run/dbus/system_bus_socket'
    return next(get_connectable_addresses(addr))


def get_bus(addr):
    if addr == 'SESSION':
        return find_session_bus()
    else:
        if addr == 'SYSTEM':
            return find_system_bus()
        return next(get_connectable_addresses(addr))


if __name__ == '__main__':
    print('System bus at:', find_system_bus())
    print('Session bus at:', find_session_bus())