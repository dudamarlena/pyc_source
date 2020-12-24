# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fast_gfk/tests/models.py
# Compiled at: 2017-07-17 11:55:56
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Foo(models.Model):
    title = models.CharField(max_length=100)


class Bar(models.Model):
    title = models.CharField(max_length=100)
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')