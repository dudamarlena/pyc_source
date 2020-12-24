# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_cli/addzone.py
# Compiled at: 2020-03-29 11:31:44
# Size of source mod 2**32: 997 bytes
"""
aedir.cli.addzone - Add a zone with two role groups for zone admins / auditors and an init tag
"""
import sys, locale
from ldap0.base import decode_list
import aedir

def main():
    """
    add the zone with parameters from command-line
    """
    logger = aedir.init_logger(log_name=(sys.argv[0]))
    try:
        zone_cn, ticket_id, zone_desc = decode_list((sys.argv[1:]),
          encoding=(locale.getdefaultlocale()[1]))
    except (IndexError, ValueError, UnicodeError):
        logger.error('Missing or wrong command-line args')
        sys.stderr.write('\n\nUsage: {} <zone name> <ticket ID> <description>\n'.format(sys.argv[0]))
        sys.exit(9)
    else:
        with aedir.AEDirObject(None) as (aedir_conn):
            zone_dn = aedir_conn.add_aezone(zone_cn, ticket_id, zone_desc)
        logger.info('Added zone entry %r', zone_dn)


if __name__ == '__main__':
    main()