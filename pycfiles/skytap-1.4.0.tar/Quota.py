# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Quota.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap quotas."""
from datetime import timedelta
from skytap.models.SkytapResource import SkytapResource

class Quota(SkytapResource):
    """One piece of quota information."""

    def __init__(self, quota_json):
        """Build the quota object.

        Args:
            quota_json (list): The quota data.
        """
        super(Quota, self).__init__(quota_json)

    def _calculate_custom_data(self):
        """Create a percentage used and time object, if applicable."""
        if self.limit is not None:
            self.data['pct'] = self.usage * 100.0 / self.limit
        if self.units == 'hours':
            self.time = timedelta(hours=self.usage)
        self.data['name'] = self.id
        return

    def __str__(self):
        """Represent object as a string."""
        quota = self.id + ' = ' + str(self.usage)
        if self.units != 'integer':
            quota += '' + self.units
        return quota