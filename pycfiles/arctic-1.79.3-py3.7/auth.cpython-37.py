# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/auth.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 846 bytes
import logging
from collections import namedtuple
from pymongo.errors import OperationFailure
logger = logging.getLogger(__name__)

def authenticate(db, user, password):
    """
    Return True / False on authentication success.

    PyMongo 2.6 changed the auth API to raise on Auth failure.
    """
    try:
        logger.debug('Authenticating {} with {}'.format(db, user))
        return db.authenticate(user, password)
    except OperationFailure as e:
        try:
            logger.debug('Auth Error %s' % e)
        finally:
            e = None
            del e

    return False


Credential = namedtuple('MongoCredentials', ['database', 'user', 'password'])

def get_auth(host, app_name, database_name):
    """
    Authentication hook to allow plugging in custom authentication credential providers
    """
    from .hooks import _get_auth_hook
    return _get_auth_hook(host, app_name, database_name)