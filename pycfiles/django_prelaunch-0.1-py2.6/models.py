# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/prelaunch/models.py
# Compiled at: 2011-05-18 01:14:38
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from prelaunch.settings import *
from shorten import ShortCode

class PrelaunchSubscriber(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField()
    referrer = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.email

    @property
    def shortcode(self):
        """ Get a shortcode for the user """
        prelaunch_digits = getattr(settings, 'PRELAUNCH_DIGITS', PRELAUNCH_DIGITS)
        prelaunch_offset = getattr(settings, 'PRELAUNCH_OFFSET', PRELAUNCH_OFFSET)
        shortcode = ShortCode(prelaunch_offset, prelaunch_digits)
        return shortcode.get_shortcode(self.id)