# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/models.py
# Compiled at: 2018-01-09 13:54:21
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jmbo.models import ModelBase
from link.models import Link
from simplemde.fields import SimpleMDEField
from sortedm2m.fields import SortedManyToManyField
from banner.styles import BANNER_STYLE_CLASSES

class Banner(ModelBase):
    """Base class for all banners"""
    link = models.ForeignKey(Link, help_text=_('Link to which this banner should redirect.'), blank=True, null=True)
    style = models.CharField(choices=[ (klass.__name__, klass.__name__) for klass in BANNER_STYLE_CLASSES
                                     ], max_length=128, default='BaseStyle')
    headline = SimpleMDEField(null=True, blank=True, help_text=_("The banner's headline."))
    body = SimpleMDEField(null=True, blank=True, help_text=_("The banner's main text content."))


class Button(models.Model):
    """Call to action handling"""
    text = models.CharField(max_length=60, help_text=_('The text to be displayed as the button label'))
    link = models.ForeignKey(Link, help_text=_('CTA link for this button'), null=True, blank=True)
    banner = SortedManyToManyField(to=Banner, related_name='buttons', null=True, blank=True)

    def __unicode__(self):
        return self.text