# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/rest_framework/group_notes.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
from rest_framework import serializers
from .list import ListField
from sentry.api.fields.actor import ActorField
from sentry.api.serializers.rest_framework.mentions import MentionsMixin

class NoteSerializer(serializers.Serializer, MentionsMixin):
    text = serializers.CharField()
    mentions = ListField(child=ActorField(), required=False)
    external_id = serializers.CharField(allow_null=True, required=False)