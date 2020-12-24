# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/plugin_enabled.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from sentry import analytics

class PluginEnabledEvent(analytics.Event):
    type = 'plugin.enabled'
    attributes = (
     analytics.Attribute('user_id'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('project_id'),
     analytics.Attribute('plugin'))


analytics.register(PluginEnabledEvent)