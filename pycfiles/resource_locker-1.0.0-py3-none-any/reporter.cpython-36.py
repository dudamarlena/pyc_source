# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/reporter/reporter.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 2846 bytes
from redis import StrictRedis
from .aspects import Aspects
import logging
tags_collection = '_TAGS'
key_template = '_TAG_{key}'
key_value_template = '{key}__{value}'

def safe(thing):
    return str(thing).strip().lower().replace('.', '-').replace(':', '-').replace('_', '-')


class RedisReporter:

    def __init__(self, client=None, bombproof=True, logger=None, **tags):
        self.client = client or StrictRedis(db=1)
        self.tags = tags
        self.logger = logger or logging.getLogger(__name__)
        self.bombproof = bombproof

    def _clear_all(self):
        self.client.flushdb()

    def _increment_all(self, tags, aspects):
        (Aspects.validate)(*list(aspects))
        (self.client.sadd)(tags_collection, *list(tags.keys()))
        for key, value in tags.items():
            value = safe(value)
            key = safe(key)
            lookup_key = key_template.format(key=key)
            self.client.sadd(lookup_key, value)
            store_key = key_value_template.format(key=key, value=value)
            for aspect, incr in aspects.items():
                if isinstance(incr, float):
                    self.client.hincrbyfloat(store_key, aspect, incr)
                else:
                    self.client.hincrby(store_key, aspect, incr)

        return len(tags) * len(aspects)

    def report(self, tags, aspects):
        try:
            request = {}
            request.update(self.tags)
            request.update(tags)
            return self._increment_all(request, aspects)
        except Exception:
            if not self.bombproof:
                raise
            else:
                self.logger.error('reporting failed')

    def lock_requested(self, **tags):
        self.report(tags, {Aspects.lock_request_count: 1})

    def lock_success(self, wait: float=None, **tags):
        self.report(tags, {Aspects.lock_acquire_count: 1, Aspects.lock_acquire_wait: wait})

    def lock_failed(self, **tags):
        self.report(tags, {Aspects.lock_acquire_fail_count: 1})

    def lock_released(self, wait: float=None, **tags):
        self.report(tags, {Aspects.lock_release_count: 1, Aspects.lock_release_wait: wait})


class DummyReporter(RedisReporter):

    def __init__(self, *args, **kwargs):
        (super().__init__)(args, client=True, **kwargs)

    def report(self, tags, aspects):
        return 0