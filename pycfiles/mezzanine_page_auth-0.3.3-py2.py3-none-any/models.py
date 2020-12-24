# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/models.py
# Compiled at: 2014-07-01 03:26:52
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from mezzanine.pages.models import Page

@python_2_unicode_compatible
class PageAuthGroup(models.Model):
    page = models.ForeignKey(Page, verbose_name=_(b'page'))
    group = models.ForeignKey(Group, verbose_name=_(b'group'), related_name=b'pages')

    class Meta:
        verbose_name = _(b'Page Auth Group')
        verbose_name_plural = _(b'Page Auth Group')
        ordering = ('group', )
        unique_together = ('page', 'group')

    def __str__(self):
        return (b'{}: {} has {}').format(self._meta.module_name, self.group.name, self.page)

    @classmethod
    def unauthorized_pages(cls, user):
        """
        Returns a list of pks of page that user is unauthorized to access
        """
        if user.is_superuser:
            return list()
        groups = user.groups.all()
        if user.is_anonymous() or len(groups) == 0:
            return list(set(cls.objects.values_list(b'page__pk', flat=True)))
        pages = cls.objects.filter(group__in=groups).values_list(b'page__pk', flat=True)
        return list(cls.objects.exclude(page__in=pages).values_list(b'page__pk', flat=True))