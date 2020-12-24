# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/sentry_mail/activity/resolved.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from .base import ActivityEmail

class ResolvedActivityEmail(ActivityEmail):

    def get_activity_name(self):
        return 'Resolved Issue'

    def get_description(self):
        return '{author} marked {an issue} as resolved'