# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fa/models.py
# Compiled at: 2012-10-01 20:16:45
from django.db import models

class FoneAstraDevice(models.Model):
    """
    Representation of a FoneAstra device.  All devices in FoneAstra apps should
    subclass this class.
    """

    class Meta:
        abstract = True
        unique_together = ('connection', 'name')

    connection = models.ForeignKey(Connection, null=False)
    name = models.CharField(blank=True, max_length=20)

    def __unicode__(self):
        return self.name