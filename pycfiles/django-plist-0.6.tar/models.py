# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steingrd/Django/django-plist/django_plist/tests/testapp/models.py
# Compiled at: 2010-05-19 01:29:02
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=64)
    date = models.DateField()

    def __unicode__(self):
        return self.title