# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/reporter/query.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 942 bytes
from redis import StrictRedis
from .reporter import tags_collection
from .reporter import key_template
from .reporter import safe
from .reporter import key_value_template
from .aspects import Aspects
import json

class Query:

    def __init__(self):
        self.client = StrictRedis(db=1)

    def all_tags(self):
        return sorted([s.decode() for s in self.client.smembers(tags_collection)])

    def all_values(self, tag):
        return sorted([s.decode() for s in self.client.smembers(key_template.format(key=(safe(tag))))])

    def all_aspects(self, tag, value):
        return {k.decode():json.loads(v) for k, v in self.client.hgetall(key_value_template.format(key=(safe(tag)), value=(safe(value)))).items()}

    def aspect(self, tag, value, aspect):
        Aspects.validate(aspect)
        return json.loads(self.client.hget(key_value_template.format(key=(safe(tag)), value=(safe(value))), aspect))