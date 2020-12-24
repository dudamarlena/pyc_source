# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/managers.py
# Compiled at: 2015-06-28 18:07:27
# Size of source mod 2**32: 1151 bytes
from __future__ import unicode_literals, absolute_import
from django.db import models
from django_hstore.query import HStoreQuerySet
from django_hstore.apps import GEODJANGO_INSTALLED

class HStoreManager(models.Manager):
    __doc__ = '\n    Object manager which enables hstore features.\n    '
    use_for_related_fields = True

    def get_queryset(self):
        return HStoreQuerySet(self.model, using=self._db)

    get_query_set = get_queryset

    def hkeys(self, attr, **params):
        return self.filter(**params).hkeys(attr)

    def hpeek(self, attr, key, **params):
        return self.filter(**params).hpeek(attr, key)

    def hslice(self, attr, keys, **params):
        return self.filter(**params).hslice(attr, keys)


if GEODJANGO_INSTALLED:
    from django.contrib.gis.db import models as geo_models
    from django_hstore.query import HStoreGeoQuerySet

    class HStoreGeoManager(geo_models.GeoManager, HStoreManager):
        __doc__ = '\n        Object manager combining Geodjango and hstore.\n        '

        def get_queryset(self):
            return HStoreGeoQuerySet(self.model, using=self._db)

        get_query_set = get_queryset