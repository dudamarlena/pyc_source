# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/djangocms-minecraft/djangocms_minecraft/cli.py
# Compiled at: 2014-08-28 00:25:59
import socket, sys
from pprint import pprint
from argparse import ArgumentParser
from query import MinecraftQuery

def main():
    parser = ArgumentParser(description='Query status of Minecraft multiplayer server', epilog='Exit status: 0 if the server can be reached, otherwise nonzero.')
    parser.add_argument('host', help='target hostname')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="don't print anything, just check if the server is running")
    parser.add_argument('-p', '--port', type=int, default=25565, help='UDP port of server\'s "query" service [25565]')
    parser.add_argument('-r', '--retries', type=int, default=3, help='retry query at most this number of times [3]')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='retry timeout in seconds [10]')
    options = parser.parse_args()
    try:
        query = MinecraftQuery(options.host, options.port, timeout=options.timeout, retries=options.retries)
        server_data = query.get_rules()
    except socket.error as e:
        if not options.quiet:
            print 'socket exception caught:', e.message
            print 'Server is down or unreachable.'
        sys.exit(1)

    if not options.quiet:
        print 'Server response data:'
        pprint(server_data)
    sys.exit(0)


if __name__ == '__main__':
    main()