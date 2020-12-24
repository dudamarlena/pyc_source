# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\page\componets\files.py
# Compiled at: 2019-12-08 19:12:08
# Size of source mod 2**32: 316 bytes
from django.db import models

class ImageFile(models.Model):
    file = models.ImageField(upload_to='images')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Image {self.name}"

    class Meta:
        verbose_name = '写真'
        verbose_name_plural = '写真'