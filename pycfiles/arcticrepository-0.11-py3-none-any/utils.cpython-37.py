# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/scripts/utils.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 1741 bytes
from __future__ import absolute_import
import logging
from ..auth import get_auth, authenticate
logger = logging.getLogger(__name__)

def do_db_auth(host, connection, db_name):
    """
    Attempts to authenticate against the mongo instance.

    Tries:
      - Auth'ing against admin as 'admin' ; credentials: <host>/arctic/admin/admin
      - Auth'ing against db_name (which may be None if auth'ing against admin above)

    returns True if authentication succeeded.
    """
    admin_creds = get_auth(host, 'admin', 'admin')
    user_creds = get_auth(host, 'arctic', db_name)
    if admin_creds is None:
        if user_creds is None:
            logger.error("You need credentials for db '%s' on '%s', or admin credentials" % (db_name, host))
            return False
        else:
            authenticate(connection[db_name], user_creds.user, user_creds.password) or logger.error("Failed to authenticate to db '%s' on '%s', using user credentials" % (db_name, host))
            return False
        return True
    if not authenticate(connection.admin, admin_creds.user, admin_creds.password):
        logger.error("Failed to authenticate to '%s' as Admin. Giving up." % host)
        return False
    authenticate(connection[db_name], user_creds.user, user_creds.password)
    return True


def setup_logging():
    """ Logging setup for console scripts
    """
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')