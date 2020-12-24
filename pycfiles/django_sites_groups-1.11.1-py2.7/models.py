# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sites_groups/models.py
# Compiled at: 2016-05-25 05:23:19
from django.db import models

class SitesGroup(models.Model):
    title = models.CharField(max_length=256, help_text='A short descriptive title.')
    sites = models.ManyToManyField('sites.Site', help_text='Sites that belong to this group.')

    class Meta:
        ordering = ('title', )

    def __unicode__(self):
        return self.title

    @property
    def site_ids(self):
        return self.sites.all().values_list('id', flat=True)