# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/base/structs.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
__all__ = ('Annotation', 'Notification')
import warnings

class Annotation(object):

    def __init__(self, label, url=None, description=None):
        self.label = label
        self.url = url
        self.description = description


class Notification(object):

    def __init__(self, event, rule=None, rules=None):
        if rule and not rules:
            rules = [
             rule]
        self.event = event
        self.rules = rules or []

    @property
    def rule(self):
        warnings.warn('Notification.rule is deprecated. Switch to Notification.rules.', DeprecationWarning)
        return self.rules[0]