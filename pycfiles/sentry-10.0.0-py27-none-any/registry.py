# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/rules/registry.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
import six
from collections import defaultdict

class RuleRegistry(object):

    def __init__(self):
        self._rules = defaultdict(list)
        self._map = {}

    def __contains__(self, rule_id):
        return rule_id in self._map

    def __iter__(self):
        for rule_type, rule_list in six.iteritems(self._rules):
            for rule in rule_list:
                yield (
                 rule_type, rule)

    def add(self, rule):
        self._map[rule.id] = rule
        self._rules[rule.rule_type].append(rule)

    def get(self, rule_id, type=None):
        cls = self._map.get(rule_id)
        if type is not None and cls not in self._rules[type]:
            return
        else:
            return cls