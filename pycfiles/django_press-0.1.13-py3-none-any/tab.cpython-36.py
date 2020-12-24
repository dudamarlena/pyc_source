# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\page\componets\tab.py
# Compiled at: 2019-12-19 21:20:55
# Size of source mod 2**32: 589 bytes
from django.db import models
from markdownx.models import MarkdownxField

class TabElement(models.Model):
    title = models.CharField(max_length=30,
      verbose_name='タブの見出し')
    content = MarkdownxField(verbose_name='タブの中身',
      help_text='Markdown、HTMLでの記述が可能です。ドラッグアンドドロップで画像の配置もできます。')

    class Meta:
        verbose_name = 'タブ要素'
        verbose_name_plural = 'タブ要素'

    def __str__(self):
        return self.title