# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-pages/facebook_pages/mixins.py
# Compiled at: 2015-01-28 07:21:18
from django.conf import settings
from django.db import models
from facebook_api.utils import get_improperly_configured_field

class PhotableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'facebook_photos' in settings.INSTALLED_APPS:
        from facebook_photos.models import Album
        albums = get_improperly_configured_field('facebook_photos', True)

        def fetch_albums(self, *args, **kwargs):
            return Album.remote.fetch_page(page=self, *args, **kwargs)

    else:
        albums = get_improperly_configured_field('facebook_photos', True)
        fetch_albums = get_improperly_configured_field('facebook_photos')