# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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