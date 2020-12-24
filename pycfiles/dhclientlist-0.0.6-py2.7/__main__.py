# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dhclientlist\__main__.py
# Compiled at: 2014-08-15 11:02:33
""" Manage the command line args to get the list, then prints the result in the desired format. """
from __init__ import get
import server, server.application, argparse, json, util, sys

class ArgumentDefaultsVoidHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _get_help_string(self, action):
        if action.default:
            return super(ArgumentDefaultsVoidHelpFormatter, self)._get_help_string(action)
        return action.help


def add_common_arguments(parser):
    parser.add_argument('-d', '--driver', dest='drivername', default=None, help='specify a driver to be used')
    parser.add_argument('-a', '--address', dest='address', default='192.168.0.1:80', help="local dhcp server's address.")
    parser.add_argument('-u', '--username', dest='username', default='admin', help="local dhcp server's username.")
    parser.add_argument('-p', '--password', dest='password', default='', help="local dhcp server's password.")
    return


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands', dest='command')
parser_list_drivers = subparsers.add_parser('list-drivers', help='list all drivers')
parser_print = subparsers.add_parser('print', help='retrieves and prints the dhcp server client list', formatter_class=ArgumentDefaultsVoidHelpFormatter)
add_common_arguments(parser_print)
parser_print.add_argument('-f', '--format', dest='format', default='texttable', choices=['json', 'texttable'], help='the format of the output list.')
parser_server = subparsers.add_parser('serve', help='starts up a HTTP(S) server on the given port', formatter_class=ArgumentDefaultsVoidHelpFormatter)
parser_server.add_argument('port', help='port that the dhclientlist HTTP(S) server will bind')
add_common_arguments(parser_server)
parser_server.add_argument('--http-username', dest='http_username', help='dhclientlist server username.')
parser_server.add_argument('--http-password', dest='http_password', help='dhclientlist server password.')
parser_server.add_argument('--debug', dest='debug', action='store_true', help='runs the server in debug mode')
args = parser.parse_args()
if args.command == 'list-drivers':
    table = util.texttable.Texttable()
    table.set_deco(util.texttable_deco)
    table.add_rows([['All drivers']] + [ [driver_name.replace('drivers.', '')] for driver_name in util.list_all_drivers() ])
    print table.draw()
elif args.command == 'serve':
    server.serve(server.application.build(get, args.address, args.username, args.password, util.drivername_to_module(args.drivername), args.http_username, args.http_password), args.port, args.debug)
elif args.command == 'print':
    try:
        result = get(args.address, args.username, args.password, util.drivername_to_module(args.drivername))
    except Exception as ex:
        print >> sys.stderr, ex
        exit(1)

    if len(result):
        if args.format == 'json':
            print json.dumps(result)
        elif args.format == 'texttable':
            print util.to_texttable(result)
    else:
        print 'No results found.'