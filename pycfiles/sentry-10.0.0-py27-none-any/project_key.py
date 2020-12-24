# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/project_key.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.serializers import Serializer, register
from sentry.loader.browsersdkversion import get_selected_browser_sdk_version, get_browser_sdk_version_choices
from sentry.models import ProjectKey

@register(ProjectKey)
class ProjectKeySerializer(Serializer):

    def serialize(self, obj, attrs, user):
        name = obj.label or obj.public_key[:14]
        d = {'id': obj.public_key, 
           'name': name, 
           'label': name, 
           'public': obj.public_key, 
           'secret': obj.secret_key, 
           'projectId': obj.project_id, 
           'isActive': obj.is_active, 
           'rateLimit': {'window': obj.rate_limit_window, 'count': obj.rate_limit_count} if obj.rate_limit_window and obj.rate_limit_count else None, 
           'dsn': {'secret': obj.dsn_private, 
                   'public': obj.dsn_public, 
                   'csp': obj.csp_endpoint, 
                   'security': obj.security_endpoint, 
                   'minidump': obj.minidump_endpoint, 
                   'unreal': obj.unreal_endpoint, 
                   'cdn': obj.js_sdk_loader_cdn_url}, 
           'browserSdkVersion': get_selected_browser_sdk_version(obj), 
           'browserSdk': {'choices': get_browser_sdk_version_choices()}, 'dateCreated': obj.date_added}
        return d