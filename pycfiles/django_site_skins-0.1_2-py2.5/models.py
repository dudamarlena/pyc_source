# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/models.py
# Compiled at: 2010-03-20 20:08:48
"""Placeholder so that tests are loaded."""
from django.contrib.sites.models import Site
from django.db import models
from skins.skin import get_skin_choices
SKINS = get_skin_choices()

class Skin(models.Model):
    name = models.CharField(max_length=20, choices=SKINS)
    site = models.ForeignKey(Site, related_name='skin')

    def __unicode__(self):
        return '%s' % self.name