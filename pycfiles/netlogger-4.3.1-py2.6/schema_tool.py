# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/pegasus/schema_tool.py
# Compiled at: 2012-03-07 16:22:22
"""
A simple command-line tool to query and set schema version 
information in a stampede database.  Will also upgrade an 
existing database to a newer schema version.

Will need to be run as a user that has CREATE | ALTER TABLE 
permissions in the database.

Requires a standard SQLALchemy connection string.
"""
__rcsid__ = '$Id: schema_tool.py 30415 2012-02-21 16:38:19Z mgoode $'
__author__ = 'Monte Goode'
import logging, sys
from netlogger.analysis.schema.schema_check import ConnHandle, SchemaCheck
from netlogger.nllog import OptionParser, get_logger, get_root_logger

def main():
    usage = "%prog {-c | -u} connString='required' mysql_engine='optional'"
    desc = (' ').join(__doc__.split())
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option('-c', '--check', dest='schema_check', action='store_true', default=False, help='Perform a schema check')
    parser.add_option('-u', '--upgrade', dest='upgrade', action='store_true', default=False, help='Upgrade database to current version.')
    (options, args) = parser.parse_args(sys.argv[1:])
    log = get_logger(__file__)
    if len(args) == 0:
        parser.print_help()
        parser.error('Option flag and connection string required.')
    if log.getEffectiveLevel() >= logging.DEBUG:
        get_root_logger().setLevel(logging.INFO)
    num_modes = (0, 1)[bool(options.schema_check)] + (0, 1)[bool(options.upgrade)]
    if num_modes > 1:
        parser.error('Choose only one option flag')
    init = {}
    for a in args:
        (k, v) = a.split('=')
        if k in ('connString', 'mysql_engine'):
            init[k] = v

    conn = ConnHandle(**init)
    s_check = SchemaCheck(conn.get_session())
    if options.schema_check:
        log.info('Executing schema check')
        s_check.check_schema()
    elif options.upgrade:
        log.info('Performing upgrade')
        s_check.upgrade()


if __name__ == '__main__':
    main()