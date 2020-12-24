# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/services/models/category.py
# Compiled at: 2013-09-08 06:03:46
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate

class Category(BaseDate):
    """
    Categories of services
    """
    name = models.CharField(_('name'), max_length=30)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        app_label = 'services'
        db_table = 'service_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return '%s' % self.name