# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/rules/conditions/reappeared_event.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.rules.conditions.base import EventCondition

class ReappearedEventCondition(EventCondition):
    label = 'An issue changes state from ignored to unresolved'

    def passes(self, event, state):
        return state.has_reappeared