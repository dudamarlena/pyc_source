# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/rules/conditions/first_seen_event.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.rules.conditions.base import EventCondition

class FirstSeenEventCondition(EventCondition):
    label = 'An issue is first seen'

    def passes(self, event, state):
        if self.rule.environment_id is None:
            return state.is_new
        else:
            return state.is_new_group_environment
            return