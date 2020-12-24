# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/serializers.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 492 bytes
from .settings import get_settings
if get_settings('TRANSLATIONS_ENABLE_API_COMMUNICATION'):
    from rest_framework import serializers
    from translation_manager.models import TranslationEntry

    class TranslationSerializer(serializers.ModelSerializer):

        class Meta:
            model = TranslationEntry
            fields = ('original', 'translation')

        def to_representation(self, obj):
            return {obj.original: obj.translation}