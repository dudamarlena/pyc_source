# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Export.py
# Compiled at: 2017-01-03 13:07:19
"""Support for Skytap VM Exports."""
import json
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource

class Export(SkytapResource):
    """One Skytap VM Export object."""

    def __init__(self, export_json):
        """Create one Export object."""
        super(Export, self).__init__(export_json)
        self.url = '/v2/exports/' + str(self.id)

    def delete(self):
        """Delete this export job."""
        Utils.info('Deleting job ' + str(self.id) + ' from queue.')
        api = ApiClient()
        response = api.rest(self.url, {}, 'DELETE')
        return response