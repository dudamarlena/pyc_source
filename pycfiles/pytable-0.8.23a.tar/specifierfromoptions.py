# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/specifierfromoptions.py
# Compiled at: 2004-08-27 02:11:58
import optparse, sys
from pytable import dbspecifier

def specifierFromOptions():
    """Load a dbspecifier from default arguments"""
    global COMMAND_LINE_SPECIFIER
    try:
        return COMMAND_LINE_SPECIFIER
    except NameError:
        pass

    parser = optparse.OptionParser()
    parser.add_option('', '--drivername', dest='drivername', help='The Database driver to use: PyPgSQL or MySQL being most common choices', type='string', metavar='DRIVER', default='PyPgSQL')
    parser.add_option('-s', '--server', dest='host', help='Database server (network address) to which to connect', type='string')
    parser.add_option('-d', '--database', dest='database', help='Database to which to connect', type='string')
    parser.add_option('-u', '--user', dest='user', help='Username to use when connecting to database', type='string')
    parser.add_option('-p', '--password', dest='password', help='Password to use when connecting to database', type='string')
    (options, args) = parser.parse_args()
    spec = dbspecifier.DBSpecifier(drivername=options.drivername, database=options.database, user=options.user, password=options.password, host=options.host)
    sys.argv[1:] = args
    COMMAND_LINE_SPECIFIER = spec
    return spec


if __name__ == '__main__':
    (spec, args) = specifierFromOptions()
    print spec
    print args