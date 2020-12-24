# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libmotop/motop.py
# Compiled at: 2014-08-20 03:31:25
"""Class imports"""
from libmotop.console import Console
from libmotop.server import Server
from libmotop.queryscreen import QueryScreen
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

from libmotop import __name__, __version__, __doc__
configFile = '/etc/motop.conf'
optionalVariables = ('username', 'password')
choices = ('status', 'replicationInfo', 'replicaSet', 'operations', 'replicationOperations')

def version():
    return __name__ + ' ' + str(__version__)


def parseArguments():
    """Create ArgumentParser instance. Return parsed arguments."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description=__doc__)
    parser.add_argument('hosts', metavar='host', nargs='*', default=('localhost:27017', ), help='address of the server or section name on the configuration file')
    parser.add_argument('-u', '--username', dest='username', help='username for authentication')
    parser.add_argument('-p', '--password', dest='password', help='password for authentication')
    parser.add_argument('-c', '--conf', dest='conf', default=configFile, help='path of configuration file')
    parser.add_argument('-V', '--version', action='version', version=version())
    parser.add_argument('-K', '--auto-kill', dest='autoKillSeconds', help='seconds to kill operations automatically')
    return parser.parse_args()


def commonServers(config, arguments):
    """First try to match servers on the config with the ones on the arguments."""
    servers = []
    for host in arguments.hosts:
        for section in config.sections():
            if section == host:
                servers.append(Server(section, **dict(config.items(section))))

    if servers:
        return servers
    if config.sections():
        return [ Server(section, **dict(config.items(section))) for section in config.sections() ]
    return [ Server(host, host, arguments.username, arguments.password) for host in arguments.hosts ]


def run():
    """Get the arguments and parse the config file. Activate console. Get servers from the config file
    or from arguments. Show the query screen."""
    arguments = parseArguments()
    config = SafeConfigParser({'username': arguments.username, 'password': arguments.password})
    config.read(arguments.conf)
    servers = commonServers(config, arguments)
    chosenServers = {}
    for choice in choices:
        if config.sections():
            chosenServers[choice] = []
            for server in servers:
                if not config.has_option(str(server), choice) or config.getboolean(str(server), choice):
                    chosenServers[choice].append(server)

        else:
            chosenServers[choice] = servers

    with Console() as (console):
        queryScreen = QueryScreen(console, chosenServers, autoKillSeconds=arguments.autoKillSeconds)
        try:
            queryScreen.action()
        except KeyboardInterrupt:
            pass