# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-m2m-history/m2m_history/test_app/models.py
# Compiled at: 2016-02-26 14:51:27
from django.db import models
from ..fields import ManyToManyHistoryField

class Publication(models.Model):
    title = models.CharField(max_length=30)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = ManyToManyHistoryField(Publication, versions=True)
    publications_no_versions = ManyToManyHistoryField(Publication, related_name='articles_no_versions')