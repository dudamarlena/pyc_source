# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/queuetools/options.py
# Compiled at: 2015-07-13 22:33:06
import optparse

def add_connection_options(parser):
    connection_group = optparse.OptionGroup(parser, 'Connection options', 'The following options define the connection to the AMQP broker.')
    connection_group.add_option('-H', '--host', action='store', default='localhost', help='host or host:port of the AMQP broker (default: %default)')
    connection_group.add_option('-U', '--userid', action='store', default='guest', help='connection username (defaut: %default)')
    connection_group.add_option('-P', '--password', action='store', default=None, help='connection password. If blank, a password will be displayed (recommended)')
    connection_group.add_option('-V', '--vhost', action='store', default='/', help='AMQ virtual host to connect to (default: %default)')
    parser.add_option_group(connection_group)
    return