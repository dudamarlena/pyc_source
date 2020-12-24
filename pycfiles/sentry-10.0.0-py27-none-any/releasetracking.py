# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/bases/releasetracking.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.plugins import Plugin2

class ReleaseTrackingPlugin(Plugin2):

    def get_plugin_type(self):
        return 'release-tracking'

    def get_release_doc_html(self, hook_url):
        raise NotImplementedError