# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/projects/thalesians/menuplaceholder/menuplaceholder/models.py
# Compiled at: 2018-04-01 02:13:50
from django.db import models
from mezzanine.pages.models import Page
from django.utils.translation import ugettext_lazy as _, ugettext

class MenuPlaceholder(Page):
    """
    This represents menu items that are placeholders, but do not actually
    represent real pages.
    """

    class Meta:
        verbose_name = _('Menu placeholder')
        verbose_name_plural = _('Menu placeholders')