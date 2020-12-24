# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cameronlowe/Development/django-zencoder/zencoder/serializers.py
# Compiled at: 2017-01-17 17:04:11
# Size of source mod 2**32: 1207 bytes
from rest_framework import serializers
from zencoder.utils.serializers import PlaceholderFieldsMixin
from .models import Source, Video

class ZencoderSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Source


class ZencoderVideoSerializer(PlaceholderFieldsMixin, serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    sources = ZencoderSourceSerializer(many=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = Video
        placeholder_fields = {'category': '', 
         'channel_logo_url': '', 
         'channel_name': '', 
         'channel_slug': '', 
         'channel_url': '', 
         'description': '', 
         'player_options': {},  'season': '', 
         'series_logo_url': '', 
         'series_name': '', 
         'series_slug': '', 
         'series_url': '', 
         'sponsor_id': None, 
         'tags': [],  'targeting': {},  'tunic_campaign_url': None}

    def get_poster_url(self, obj):
        return getattr(obj, 'poster', '')

    def get_title(self, obj):
        return getattr(obj, 'name', '')