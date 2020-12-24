# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/drilldown/tests/models.py
# Compiled at: 2009-10-22 11:51:54
from django.db import models
from django.contrib.auth.models import User, Group, AnonymousUser
from softwarefabrica.django.common.models import *

class Author(CommonOwnedModel):
    __module__ = __name__
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True, db_index=True)
    death_date = models.DateField(blank=True, null=True, db_index=True)

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        __module__ = __name__
        ordering = ['last_name', 'first_name', 'created']

    def get_absolute_url(self):
        return '/author/%s/' % self.pk


class Category(CommonOwnedModel):
    __module__ = __name__
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(db_index=True, unique=True)


COVER_TYPE = (
 ('h', 'hard cover'), ('p', 'paperback'))
CONDITION_TYPE = (
 ('a', 'ancient'), ('u', 'used'), ('n', 'new'))

class Book(CommonOwnedModel):
    __module__ = __name__
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(db_index=True, unique=True)
    excerpt = models.TextField(blank=True)
    author = models.ForeignKey(Author, db_index=True)
    year = models.IntegerField(blank=True, default=2009)
    bought = models.DateField(blank=True, null=True, db_index=True)
    keywords = models.CharField(max_length=200, blank=True, db_index=True)
    cover = models.CharField(max_length=2, choices=COVER_TYPE, blank=True, db_index=True)
    condition = models.CharField(max_length=2, choices=CONDITION_TYPE, blank=False, db_index=True)
    categories = models.ManyToManyField(Category, db_index=True, null=True, blank=True)
    weight = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        __module__ = __name__
        ordering = ['title', 'created', 'uuid']

    class SFApp:
        __module__ = __name__
        drilldown_fields = ('title', 'desc', 'slug', 'author', 'year', 'bought', 'keywords',
                            'cover', 'condition', 'categories', 'weight', 'active',
                            'createdby', 'created', 'modifiedby', 'modified')

    def get_absolute_url(self):
        return '/book/%s/' % self.pk