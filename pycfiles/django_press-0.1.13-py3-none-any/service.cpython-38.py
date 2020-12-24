# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\page\componets\service.py
# Compiled at: 2019-12-08 19:12:08
# Size of source mod 2**32: 604 bytes
from django.db import models

class Product(models.Model):
    icon = models.CharField(max_length=100,
      verbose_name='icon class',
      help_text='https://icofont.com/icons 参照',
      default='icofont icofont-light-bulb')
    name = models.CharField(max_length=30,
      verbose_name='サービス名')
    description = models.TextField(verbose_name='説明')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '紹介する系'
        verbose_name_plural = '紹介する系'