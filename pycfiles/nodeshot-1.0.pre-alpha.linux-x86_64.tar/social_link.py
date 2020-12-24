# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/profiles/models/social_link.py
# Compiled at: 2015-03-02 10:21:03
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from . import Profile

class SocialLink(BaseDate):
    """
    External links like website or social network profiles
    """
    user = models.ForeignKey(Profile, verbose_name=_('user'))
    url = models.URLField(_('url'))
    description = models.CharField(_('description'), max_length=128, blank=True)

    class Meta:
        ordering = [
         'id']
        app_label = 'profiles'
        db_table = 'profiles_social_links'
        unique_together = ('user', 'url')

    def __unicode__(self):
        return self.url