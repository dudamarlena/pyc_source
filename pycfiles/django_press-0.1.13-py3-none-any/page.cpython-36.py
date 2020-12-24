# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\page\page.py
# Compiled at: 2020-01-08 02:33:01
# Size of source mod 2**32: 1584 bytes
from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=100)
    in_nav = models.BooleanField(default=False)
    path = models.CharField(max_length=100, unique=True, blank=True)
    parent_page = models.ForeignKey(to='self',
      on_delete=(models.SET_NULL),
      verbose_name='このページに親となるページ',
      blank=True,
      null=True,
      help_text='パンくずリストの作成、SEO対策となります。')
    publish = models.BooleanField('公開設定',
      default=True)

    class Meta:
        verbose_name = 'Webページ'
        verbose_name_plural = 'Webページ'

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.path is None:
            self.path = self.title
        super().save(force_insert, force_update, using, update_fields)

    @property
    def url(self):
        return '/' + self.path

    @property
    def a_tag(self):
        return f'a href="{self.url}" style="color: inherit">{self.title}</a>'

    @property
    def get_parents_node(self):
        if self.parent_page:
            return self.parent_page._get_parents_node([self])
        else:
            return [
             self]

    def _get_parents_node(self, node):
        if self.parent_page:
            return self.parent_page._get_parents_node(node + [self])
        else:
            return reversed(node + [self])