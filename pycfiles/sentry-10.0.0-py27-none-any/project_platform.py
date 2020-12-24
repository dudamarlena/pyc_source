# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/project_platform.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.serializers import register, Serializer
from sentry.models import ProjectPlatform

@register(ProjectPlatform)
class ProjectPlatformSerializer(Serializer):
    """
    Tracks usage of a platform for a given project.

    Note: This model is used solely for analytics.
    """

    def serialize(self, obj, attrs, user):
        return {'platform': obj.platform, 'dateCreated': obj.date_added}