# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/sentry_mail/activity/note.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from .base import ActivityEmail

class NoteActivityEmail(ActivityEmail):

    def get_context(self):
        return {}

    def get_template(self):
        return 'sentry/emails/activity/note.txt'

    def get_html_template(self):
        return 'sentry/emails/activity/note.html'