# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/tests/testapp/models.py
# Compiled at: 2015-06-23 21:40:14
from django.db import models
from django.db.models.query import QuerySet
from django_toolkit.db.models import QuerySetManager

class ModelWithChainedQuerySet(models.Model):
    foo = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    objects = QuerySetManager()

    def __unicode__(self):
        return '%s' % self.pk

    class QuerySet(QuerySet):

        def is_foo(self):
            return self.filter(foo=True)

        def is_bar(self):
            return self.filter(bar=True)

        def is_not_foo(self):
            return self.filter(foo=False)

        def is_not_bar(self):
            return self.filter(bar=False)