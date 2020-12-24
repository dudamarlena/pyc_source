# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_cli/passwd.py
# Compiled at: 2020-03-29 11:31:44
# Size of source mod 2**32: 1718 bytes
"""
Sets the password of the specified aeUser/aeService or aeHost entry
referenced by uid or host attribute

This script must run locally on a Æ-DIR provider
"""
import sys, getpass
from ldap0 import LDAPError
import aedir

def main():
    """
    set password for entry referenced by name
    """
    logger = aedir.init_logger(log_name=(sys.argv[0]))
    try:
        arg_value = sys.argv[1]
    except IndexError:
        sys.stderr.write('Usage: {} <username|hostname>\n'.format(sys.argv[0]))
        sys.exit(9)
    else:
        with aedir.AEDirObject(None) as (aedir_conn):
            logger.debug('successfully connected to %r as %r', aedir_conn.uri, aedir_conn.whoami_s())
            new_password1 = getpass.getpass('Enter new password for {} (empty generates password): '.format(arg_value))
            if new_password1:
                new_password2 = getpass.getpass('repeat password: ')
                if new_password1 != new_password2:
                    sys.stderr.write('2nd input for new password differs!\n')
                    sys.exit(1)
            else:
                new_password2 = None
            try:
                entry_dn, new_pw = aedir_conn.set_password(arg_value, new_password2)
            except LDAPError as ldap_err:
                try:
                    logger.error('LDAPError setting password: %s', ldap_err)
                    sys.exit(1)
                finally:
                    ldap_err = None
                    del ldap_err

            else:
                if new_password2 is None:
                    sys.stdout.write('Generated password: %s\n' % new_pw)
                logger.info('Successfully set password of entry %r', entry_dn)


if __name__ == '__main__':
    main()