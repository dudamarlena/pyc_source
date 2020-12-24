# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/apipool-project/apipool/manager.py
# Compiled at: 2018-08-21 17:17:02
# Size of source mod 2**32: 4445 bytes
"""
built-in stats collector service for api usage and status.
"""
import sys, random
from collections import OrderedDict
from sqlalchemy_mate import engine_creator
from .apikey import ApiKey
from .stats import StatusCollection, StatsCollector

def validate_is_apikey(obj):
    if not isinstance(obj, ApiKey):
        raise TypeError


class ApiCaller(object):

    def __init__(self, apikey, apikey_manager, call_method, reach_limit_exc):
        self.apikey = apikey
        self.apikey_manager = apikey_manager
        self.call_method = call_method
        self.reach_limit_exc = reach_limit_exc

    def __call__(self, *args, **kwargs):
        try:
            res = (self.call_method)(*args, **kwargs)
            self.apikey_manager.stats.add_event(self.apikey.primary_key, StatusCollection.c1_Success.id)
            return res
        except self.reach_limit_exc as e:
            self.apikey_manager.remove_one(self.apikey.primary_key)
            self.apikey_manager.stats.add_event(self.apikey.primary_key, StatusCollection.c9_ReachLimit.id)
            raise e
        except Exception as e:
            self.apikey_manager.stats.add_event(self.apikey.primary_key, StatusCollection.c5_Failed.id)
            raise e


class DummyClient(object):

    def __init__(self):
        self._apikey_manager = None

    def __getattr__(self, item):
        apikey = self._apikey_manager.random_one()
        call_method = getattr(apikey._client, item)
        return ApiCaller(apikey=apikey,
          apikey_manager=(self._apikey_manager),
          call_method=call_method,
          reach_limit_exc=(self._apikey_manager.reach_limit_exc))


class ApiKeyManager(object):
    _settings_api_client_class = None

    def __init__(self, apikey_list, reach_limit_exc, db_engine=None):
        for apikey in apikey_list:
            validate_is_apikey(apikey)

        if db_engine is None:
            db_engine = engine_creator.create_sqlite()
        self.stats = StatsCollector(engine=db_engine)
        self.stats.add_all_apikey(apikey_list)
        self.apikey_chain = OrderedDict()
        for apikey in apikey_list:
            self.add_one(apikey, upsert=False)

        self.archived_apikey_chain = OrderedDict()
        self.reach_limit_exc = reach_limit_exc
        self.dummyclient = DummyClient()
        self.dummyclient._apikey_manager = self

    def add_one(self, apikey, upsert=False):
        validate_is_apikey(apikey)
        primary_key = apikey.primary_key
        do_insert = False
        if primary_key in self.apikey_chain:
            if upsert:
                do_insert = True
        else:
            do_insert = True
        if do_insert:
            try:
                apikey.connect_client()
                self.apikey_chain[primary_key] = apikey
            except Exception as e:
                sys.stdout.write("\nCan't create api client with {}, error: {}".format(apikey.primary_key, e))

        self.stats.add_all_apikey([apikey])

    def fetch_one(self, primary_key):
        return self.apikey_chain[primary_key]

    def remove_one(self, primary_key):
        apikey = self.apikey_chain.pop(primary_key)
        self.archived_apikey_chain[primary_key] = apikey
        return apikey

    def random_one(self):
        return random.choice(list(self.apikey_chain.values()))

    def check_usable(self):
        for primary_key, apikey in self.apikey_chain.items():
            if apikey.is_usable():
                self.stats.add_event(primary_key, StatusCollection.c1_Success.id)
            else:
                self.remove_one(primary_key)
                self.stats.add_event(primary_key, StatusCollection.c5_Failed.id)

        if len(self.apikey_chain) == 0:
            sys.stdout.write("\nThere's no API Key usable!")
        else:
            if len(self.archived_apikey_chain) == 0:
                sys.stdout.write('\nAll API Key are usable.')
            else:
                sys.stdout.write('\nThese keys are not usable:')
                for key in self.archived_apikey_chain:
                    sys.stdout.write('\n    %s: %r' % (key, apikey))