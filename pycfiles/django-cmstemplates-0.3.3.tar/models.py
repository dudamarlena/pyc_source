# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/models.py
# Compiled at: 2016-02-24 04:47:14
from __future__ import unicode_literals, print_function
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cmstemplates import managers

@python_2_unicode_compatible
class TemplateGroup(models.Model):
    name = models.CharField(_(b'Template group name'), max_length=255)
    description = models.TextField(_(b'Short description'), blank=True, default=b'')

    class Meta:
        verbose_name = _(b'Template group')
        verbose_name_plural = _(b'Template groups')

    def __str__(self):
        if self.description:
            return b'%s - %s' % (self.name, self.description)
        return self.name

    @property
    def cache_key(self):
        return (b'cmstemplates:group:{}').format(self.name)


@python_2_unicode_compatible
class Template(models.Model):
    name = models.CharField(_(b'Template name'), max_length=255, help_text=_(b'Template name, for example, "headline"'))
    group = models.ForeignKey(TemplateGroup, verbose_name=_(b'Group'), related_name=b'templates')
    weight = models.IntegerField(_(b'Output order'), default=0)
    content = models.TextField(_(b'Content'))
    is_active = models.BooleanField(_(b'Active'), default=True)
    only_for_superuser = models.BooleanField(_(b'Only for superuser'), default=False)
    objects = managers.TemplateQuerySet().as_manager()

    class Meta:
        verbose_name = _(b'Template')
        verbose_name_plural = _(b'Template')
        ordering = [b'weight']

    def __str__(self):
        return self.name

    def render(self):
        if self.only_for_superuser:
            html = (b'').join([
             b'{% if request.user.is_superuser %}',
             self.content,
             b'{% endif %}'])
            return html
        return self.content