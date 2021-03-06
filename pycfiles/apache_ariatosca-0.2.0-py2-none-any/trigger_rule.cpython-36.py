# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/trigger_rule.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 1653 bytes
from __future__ import unicode_literals
from builtins import object
from typing import Set

class TriggerRule(object):
    ALL_SUCCESS = 'all_success'
    ALL_FAILED = 'all_failed'
    ALL_DONE = 'all_done'
    ONE_SUCCESS = 'one_success'
    ONE_FAILED = 'one_failed'
    NONE_FAILED = 'none_failed'
    NONE_SKIPPED = 'none_skipped'
    DUMMY = 'dummy'
    _ALL_TRIGGER_RULES = set()

    @classmethod
    def is_valid(cls, trigger_rule):
        return trigger_rule in cls.all_triggers()

    @classmethod
    def all_triggers(cls):
        if not cls._ALL_TRIGGER_RULES:
            cls._ALL_TRIGGER_RULES = {getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr))}
        return cls._ALL_TRIGGER_RULES