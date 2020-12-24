# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/passwordless/token_store.py
# Compiled at: 2017-11-22 16:02:35
import abc
from propjockey.util import mongoconnect

class TokenStore(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        pass

    @abc.abstractmethod
    def store_or_update(self, token, userid, ttl=600, origin=None):
        pass

    @abc.abstractmethod
    def invalidate_token(self, userid):
        pass

    @abc.abstractmethod
    def get_by_userid(self, userid):
        pass


class MemoryTokenStore(TokenStore):
    STORE = {}

    def store_or_update(self, token, userid, ttl=600, origin=None):
        self.STORE[userid] = token

    def invalidate_token(self, userid):
        del self.STORE[userid]

    def get_by_userid(self, userid):
        return self.STORE.get(userid, None)


class MongoTokenStore(TokenStore):

    def __init__(self, config):
        ts_config = config['tokenstore_client']
        self.client = mongoconnect(ts_config)
        self.db = self.client[ts_config['database']]
        self.collection = self.db[ts_config['collection']]
        self.collection.create_index('userid')

    def store_or_update(self, token, userid, ttl=None, origin=None):
        if not token or not userid:
            return False
        self.collection.replace_one({'userid': userid}, {'userid': userid, 'token': token}, upsert=True)

    def invalidate_token(self, userid):
        self.collection.delete_many({'userid': userid})

    def get_by_userid(self, userid):
        usertoken = self.collection.find_one({'userid': userid})
        if usertoken:
            return usertoken.get('token')
        else:
            return


TOKEN_STORES = {'memory': MemoryTokenStore, 
   'mongo': MongoTokenStore}