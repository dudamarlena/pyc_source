# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/arpamynt/mezzanine_faq/models.py
# Compiled at: 2016-01-12 18:39:38
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.models import Orderable
from mezzanine.pages.models import Page

class FaqPage(Page):

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')


class FaqQuestion(Orderable):
    page = models.ForeignKey(FaqPage)
    question = models.TextField(_('Question'))
    answer = models.TextField(_('Answer'))

    class Meta:
        order_with_respect_to = 'page'
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')