# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/PublishedService.py
# Compiled at: 2016-12-16 14:55:45
"""Support for a published service resource in Skytap."""
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource

class PublishedService(SkytapResource):
    """One published service object."""

    def delete(self):
        """Delete a service. Warning: Cannot be undone."""
        Utils.info('Deleting published service: ' + str(self.id))
        api = ApiClient()
        response = api.rest(self.url, {}, 'DELETE')
        return response