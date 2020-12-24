# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/actor.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer
from sentry.models import User, Team

class ActorSerializer(Serializer):

    def serialize(self, obj, attrs, user, **kwargs):
        if isinstance(obj, User):
            actor_type = 'user'
            name = obj.get_display_name()
            context = {'email': obj.email}
        elif isinstance(obj, Team):
            actor_type = 'team'
            name = obj.slug
            context = {}
        else:
            raise AssertionError('Invalid type to assign to: %r' % type(obj))
        context.update({'type': actor_type, 'id': six.text_type(obj.id), 'name': name})
        return context