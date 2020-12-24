# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/sentry_mail/activity/regression.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.utils.html import escape
from sentry.utils.http import absolute_uri
from .base import ActivityEmail

class RegressionActivityEmail(ActivityEmail):

    def get_activity_name(self):
        return 'Regression'

    def get_description(self):
        data = self.activity.data
        if data.get('version'):
            version_url = ('/organizations/{}/releases/{}/').format(self.organization.slug, data['version'])
            return (
             '{author} marked {an issue} as a regression in {version}', {'version': data['version']},
             {'version': ('<a href="{}">{}</a>').format(absolute_uri(version_url), escape(data['version']))})
        return '{author} marked {an issue} as a regression'