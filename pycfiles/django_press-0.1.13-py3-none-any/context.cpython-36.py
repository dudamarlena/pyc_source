# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\context.py
# Compiled at: 2019-12-06 05:11:07
# Size of source mod 2**32: 531 bytes
from django.db import models

class Context(models.Model):
    key = models.CharField(max_length=500, unique=True, blank=False, null=False)
    value = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.value:
            self.value = self.key
        super().save(force_insert, force_update, using, update_fields)