# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/keystoneredis/token.py
# Compiled at: 2013-02-13 14:17:43
"""Redis backends for the various services."""
import dateutil.parser, copy
from keystone import exception
from keystone.openstack.common import timeutils
from keystone import token
from keystone.openstack.common import jsonutils
from common.session import RedisSession
from common import keys

class Token(RedisSession, token.Driver):

    def __init__(self, *args, **kwargs):
        RedisSession.__init__(self, *args, **kwargs)

    def flush_all(self):
        self.conn.flushall_everywhere()

    def get_token(self, token_id):
        token_key = keys.token(token_id)
        value = self.readonly.get(token_key)
        if value:
            token = jsonutils.loads(value)
            if token.get('expires', None) is not None:
                token['expires'] = dateutil.parser.parse(token['expires'])
                if token['expires'] > timeutils.utcnow():
                    return token
            else:
                return token
        raise exception.TokenNotFound(token_id=token_id)
        return

    def _set_keys(self, user_id, token_id, json_data, ttl_seconds):
        commands = []
        token_key = keys.token(token_id)
        if user_id:
            user_key = keys.usertoken(user_id['id'], token_id)
        if ttl_seconds is None:
            commands.append(('set', (token_key, json_data)))
            if user_id:
                commands.append(('set', (user_key, '')))
        else:
            commands.append(('setex', (token_key, ttl_seconds, json_data)))
            if user_id:
                commands.append(('setex', (user_key, ttl_seconds, '')))
        self.conn.pipe_everywhere(commands)
        return

    def create_token(self, token_id, data):
        data_copy = copy.deepcopy(data)
        user_id = data_copy.get('user', None)
        if 'expires' not in data_copy:
            data_copy['expires'] = self._get_default_expire_time()
        json_data = jsonutils.dumps(data_copy)
        self._set_keys(user_id, token_id, json_data, self.ttl_seconds)
        return data_copy

    def _delete_keys(self, user_id, token_id):
        commands = []
        token_key = keys.token(token_id)
        commands.append(('delete', (token_key,)))
        if user_id is not None:
            user_key = keys.usertoken(user_id['id'], token_id)
            commands.append(('delete', (user_key,)))
        commands.append(('sadd', (keys.revoked(), token_id)))
        return self.conn.pipe_everywhere(commands)[0]

    def delete_token(self, token_id):
        data = self.get_token(token_id)
        user_id = data.get('user', None)
        if not self._delete_keys(user_id, token_id):
            raise exception.TokenNotFound(token_id=token_id)
        return

    def list_tokens(self, user_id, tenant=None):
        pattern = keys.usertoken(user_id, '*')
        user_keys = self.readonly.keys(pattern)
        return [ keys.parse_usertoken(key)[1] for key in user_keys ]

    def list_revoked_tokens(self):
        return [ {'id': s} for s in self.readonly.smembers(keys.revoked()) ]


class TokenNoList(Token):

    def _set_keys(self, user_id, token_id, json_data, ttl_seconds):
        token_key = keys.token(token_id)
        if ttl_seconds is None:
            self.conn.set_everywhere(token_key, json_data)
        else:
            self.conn.setex_everywhere(token_key, ttl_seconds, json_data)
        return

    def delete_token(self, token_id):
        if not self._delete_keys(None, token_id):
            raise exception.TokenNotFound(token_id=token_id)
        return

    def list_tokens(self, user_id):
        raise exception.NotImplemented()

    def list_revoked_tokens(self):
        raise exception.NotImplemented()