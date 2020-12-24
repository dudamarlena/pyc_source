# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football365/models.py
# Compiled at: 2013-05-21 11:00:49
from django.db import models

class Call(models.Model):
    title = models.CharField(max_length=256, help_text='A short descriptive title for your reference.')
    call_type = models.CharField(max_length=32, choices=(
     ('table', 'Table'),
     ('fixtures', 'Fixtures'),
     ('results', 'Results'),
     ('live', 'Live scores')))
    football365_service_id = models.PositiveIntegerField(help_text='Internal service identifier used by Football365')
    client_id = models.CharField(max_length=32, null=True, blank=True, help_text='Override the account name in settings on a per-call basis')
    url = models.URLField(null=True, blank=True, help_text='Override the url in settings on a per-call basis')

    class Meta:
        ordering = ('title', )

    def __unicode__(self):
        return self.title