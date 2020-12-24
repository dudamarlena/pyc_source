# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marple/models.py
# Compiled at: 2018-06-30 09:10:07
# Size of source mod 2**32: 378 bytes
import hashlib, re
from django.db import models
from django.contrib.postgres.fields import JSONField

class MarpleItem(models.Model):
    type = models.SlugField()
    name = models.CharField(max_length=255, default='')
    data = JSONField()

    class Meta:
        ordering = [
         'type', 'name']

    def __str__(self):
        return '%s [%s]' % (self.name, self.type)