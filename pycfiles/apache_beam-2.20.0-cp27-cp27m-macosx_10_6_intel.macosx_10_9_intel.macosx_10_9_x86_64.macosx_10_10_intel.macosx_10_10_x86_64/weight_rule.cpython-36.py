# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/weight_rule.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 1500 bytes
from __future__ import unicode_literals
from builtins import object
from typing import Set

class WeightRule(object):
    DOWNSTREAM = 'downstream'
    UPSTREAM = 'upstream'
    ABSOLUTE = 'absolute'
    _ALL_WEIGHT_RULES = set()

    @classmethod
    def is_valid(cls, weight_rule):
        return weight_rule in cls.all_weight_rules()

    @classmethod
    def all_weight_rules(cls):
        if not cls._ALL_WEIGHT_RULES:
            cls._ALL_WEIGHT_RULES = {getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr))}
        return cls._ALL_WEIGHT_RULES