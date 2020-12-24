# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christianschuermann/Documents/Repositories/django-translator/translator/models.py
# Compiled at: 2020-01-22 10:12:27
# Size of source mod 2**32: 819 bytes
import django.core.cache as cache
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from translator.util import get_key

class Translation(models.Model):
    key = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.key

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        all_translation_keys = Translation.objects.all().values_list('key', flat=True)
        for l in settings.LANGUAGES:
            cache.delete_many([get_key(l[0], k) for k in all_translation_keys])
        else:
            return super(Translation, self).save(force_insert, force_update, using, update_fields)