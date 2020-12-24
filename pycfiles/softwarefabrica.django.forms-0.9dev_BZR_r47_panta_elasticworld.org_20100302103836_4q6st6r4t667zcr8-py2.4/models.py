# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/forms/tests/models.py
# Compiled at: 2008-12-22 09:11:43
from django.db import models

class Author(models.Model):
    __module__ = __name__
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_year = models.IntegerField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)

    class Meta:
        __module__ = __name__
        ordering = ['last_name', 'name']

    def get_absolute_url(self):
        return '/authors/%s/' % self.id

    def get_create_url(cls):
        return '/authors/new/'

    get_create_url = classmethod(get_create_url)

    def get_edit_url(self):
        return '/authors/%s/edit' % self.id

    def get_list_url(cls):
        return '/authors/'

    get_list_url = classmethod(get_list_url)


class Book(models.Model):
    __module__ = __name__
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=32, blank=True)
    author = models.ForeignKey(Author, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        if self.author:
            return '%s (%s)' % (self.title, self.author)
        return '%s' % self.title

    class Meta:
        __module__ = __name__
        ordering = ['title']


class BookRent(models.Model):
    __module__ = __name__
    book = models.ForeignKey(Book)
    when = models.DateTimeField()

    def __unicode__(self):
        return '%s - %s' % (self.book, self.when)

    class Meta:
        __module__ = __name__
        ordering = ['-when', 'book', '-id']