# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbe/authentication.py
# Compiled at: 2015-11-15 14:47:58
# Size of source mod 2**32: 7440 bytes
"""
The authentication module is responsible for taking log in credentials an establish a session.
Session data is saved in the Session collection.
"""
from mbe.misc.schema_mongodb import mbe_object_id
__author__ = 'Nicklas Boerjesson'
import hashlib
from mbe.constants import schemaId_user
import datetime
from decorator import decorator
from mbe.misc.aspect_utilities import alter_function_parameter_and_call
from inspect import getfullargspec
_authentication = None

def init_authentication(_database_access):
    """
    Initializes the global authentication object

    :param _database_access: A database access instance that provides access to the node collection (users)
    :return: an instance of the global authentication object
    """
    global _authentication
    _authentication = Authentication(_database_access)
    return _authentication


def check_session(_session_id):
    """
       Global convenience function, see Authentication.check_session

       :param _session_id: The session Id.

    """
    if _authentication is None:
        raise AuthenticationError('check_session: No authentication object initialized. Call init_authentication.')
    return _authentication.check_session(_session_id)


def login(_credentials):
    """
       Global convenience function, see Authentication.logout

       :param _credentials: An MBE credentials package.

    """
    if _authentication is None:
        raise AuthenticationError('password_login: No authentication object initialized. Call init_authentication.')
    return _authentication.login(_credentials)


def logout(_session_id):
    """
       Global convenience function, see Authentication.logout

       :param _session_id: The session Id

    """
    if _authentication is None:
        raise AuthenticationError('session logout: No authentication object initialized. Call init_authentication.')
    return _authentication.logout(_session_id)


def check_session_aspect(func, *args, **kwargs):
    """
    The authentication aspect code, provides an aspect for the aop_check_session decorator

    """
    _argument_specifications = getfullargspec(func)
    try:
        arg_idx = _argument_specifications.args.index('_session_id')
    except:
        raise Exception('Authentication aspect for "' + func.__name__ + '": No _session_id parameter')

    _user = check_session(args[arg_idx])
    return alter_function_parameter_and_call(func, args, kwargs, '_user', _user)


def aop_check_session(f):
    """
        A session validation decorator, searches that parameters for _session_id and checks that session
    """
    return decorator(check_session_aspect, f)


class AuthenticationError(Exception):
    __doc__ = 'Exception class for authentication errors'


class Authentication:
    __doc__ = '\n    The authentication class is the central entity for authentication in MBE.\n    It handles login, logout and session validation.\n    '

    def __init__(self, _database_access):
        """
        The Authentication class need access to the database for user information.
        :param _database_access: Database access object
        """
        self._da = _database_access

    def check_session(self, _session_id):
        """
        Checks if a session_id is valid and returns the user object
        Otherwise raises an AuthenticationError,

        :param _session_id: A session_id, format is a MongoDB objectId.
        :return: A user object

        """
        _session_cond = {'conditions': {'_id': mbe_object_id(_session_id)},  'collection': 'session'}
        _sessions = self._da.find(_session_cond)
        if len(_sessions) > 0:
            if len(_sessions) > 1:
                raise Exception('password_login error: Multiple users returned by user query.')
            _user_condition = {'conditions': {'_id': mbe_object_id(_sessions[0]['user_id']),  'schemaId': schemaId_user},  'collection': 'node'}
            _users = list(self._da.find(_user_condition))
            if len(_users) > 0:
                return _users[0]
            raise AuthenticationError('Authentication failed. The user associated with the session has been removed.\nSessionId: ' + str(_session_id))
        else:
            raise AuthenticationError('Authentication failed for sessionId : ' + str(_session_id))

    def login(self, _credentials):
        """
        Takes a credentials object and logs in. Returns a tuple with a session_id and a user object if successful.
        Otherwise raises an AuthenticationError,
        If user is already logged in, that session is destroyed and this one created.

        :param _credentials: A structure containing credentials
        :return: A tuple with a session_id and a user object

        """
        if 'usernamePassword' in _credentials:
            _cred_condition = {'conditions': {'credentials.usernamePassword.username': _credentials['usernamePassword']['username'], 
                            'credentials.usernamePassword.password': hashlib.md5(_credentials['usernamePassword']['password'].encode('utf-8')).hexdigest()}, 
             'collection': 'node'}
            _users = self._da.find(_cred_condition)
            if len(_users) > 0:
                if len(_users) > 1:
                    raise Exception('password_login error: Multiple users returned by user query.')
                _user = _users[0]
                _session_data = {'createdWhen': str(datetime.datetime.utcnow()), 
                 'user_id': str(_user['_id']), 
                 'schemaId': 'db07fe92-a9bd-4791-86ab-b695397f9397'}
                _session_id = self._da.save(_session_data, _user)
                return (
                 _session_id, _user)
            raise AuthenticationError('login error: Invalid login/username combination.')
        else:
            if len(_credentials) > 0:
                raise AuthenticationError('login error: Invalid authentication scheme "' + _credentials[0] + '"')
            else:
                raise AuthenticationError('login error: Invalid authentication structure (empty)')

    def logout(self, _session_id):
        """
        Logs out the session

        :param _session_id: The session Id
        :return:

        """
        _remove_cond = {'conditions': {'_id': mbe_object_id(_session_id)},  'collection': 'session'}
        self._da.remove_condition(_remove_cond, None)