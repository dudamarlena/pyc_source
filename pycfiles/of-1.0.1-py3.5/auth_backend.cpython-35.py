# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/broker/lib/auth_backend.py
# Compiled at: 2016-09-15 19:50:18
# Size of source mod 2**32: 3081 bytes
"""
This module contains the MongoDBAuthBackend

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import datetime, hashlib
from of.broker.lib.schema_mongodb import of_object_id
from of.common.security.authentication import AuthenticationBackend

class MongoDBAuthBackend(AuthenticationBackend):
    __doc__ = '\n    The MongoDBAuthBackend class implements the AuthenticationBackend, and provides a mongodb-based\n    authentication backend for the Optimal Framework\n    '
    db_access = None

    def __init__(self, _db_access):
        self.db_access = _db_access

    def get_session(self, _session_id):
        _session_cond = {'conditions': {'_id': of_object_id(_session_id)}, 
         'collection': 'session'}
        _sessions = self.db_access.find(_session_cond)
        if len(_sessions) > 0:
            if len(_sessions) > 1:
                raise Exception('session check: Multiple users returned by user query for ' + _session_id)
            return _sessions[0]
        else:
            return

    def get_user(self, _user_id):
        _user_condition = {'conditions': {'_id': of_object_id(_user_id), 'schemaRef': 'ref://of.node.user'}, 
         'collection': 'node'}
        _users = list(self.db_access.find(_user_condition))
        if len(_users) > 0:
            if len(_users) > 1:
                raise Exception('get user: Multiple users returned by user query for ' + _user_id)
            return _users[0]
        else:
            return

    def authenticate_username_password(self, _credentials):
        _cred_condition = {'conditions': {'credentials.usernamePassword.username': _credentials['usernamePassword']['username'], 
                        'credentials.usernamePassword.password': hashlib.md5(_credentials['usernamePassword']['password'].encode('utf-8')).hexdigest()}, 
         
         'collection': 'node'}
        _users = self.db_access.find(_cred_condition)
        if len(_users) > 0:
            if len(_users) > 1:
                raise Exception('password_login error: Multiple users returned by user query.')
            _user = _users[0]
            _session_data = {'createdWhen': str(datetime.datetime.utcnow()), 
             'user_id': str(_user['_id']), 
             'schemaRef': 'ref://of.session'}
            _session_id = self.db_access.save(_session_data, _user)
            return (
             _session_id, _user)
        else:
            return (None, None)

    def logout(self, _session_id):
        _remove_cond = {'conditions': {'_id': of_object_id(_session_id)}, 
         'collection': 'session'}
        self.db_access.remove_condition(_remove_cond, None)