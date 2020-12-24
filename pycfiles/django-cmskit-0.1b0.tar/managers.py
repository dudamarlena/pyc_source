# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/products/managers.py
# Compiled at: 2012-10-09 05:01:17
from datetime import datetime
from django.db import models

class ProductQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(publish=True)

    def translation(self, lang):
        return eval('self.exclude(slug_' + lang + '=None)')


class ProductManager(models.Manager):

    def get_query_set(self):
        return ProductQuerySet(self.model, using=self._db)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)