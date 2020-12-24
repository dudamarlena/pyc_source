# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/models.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from djblets.db.fields import JSONField

@python_2_unicode_compatible
class Tool(models.Model):
    """Information about a tool installed on a worker.

    Each entry in the database will be unique for the values of `entry_point`
    and `version`. Any backwards incompatible changes to a Tool will result
    in a version bump, allowing multiple versions of a tool to work with a
    Review Board instance.
    """
    name = models.CharField(max_length=128, blank=False)
    entry_point = models.CharField(max_length=128, blank=False)
    version = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=512, default=b'', blank=True)
    enabled = models.BooleanField(default=True)
    in_last_update = models.BooleanField()
    timeout = models.IntegerField(blank=True, null=True)
    working_directory_required = models.BooleanField(default=False)
    tool_options = JSONField()

    def __str__(self):
        """Return a string representation of the tool.

        Returns:
            unicode:
            The text representation for this model.
        """
        return b'%s - v%s' % (self.name, self.version)

    class Meta:
        unique_together = ('entry_point', 'version')