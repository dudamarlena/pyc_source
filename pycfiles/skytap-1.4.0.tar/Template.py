# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Template.py
# Compiled at: 2016-12-16 14:55:45
"""Support for an Template resource in Skytap."""
import json
from skytap.framework.ApiClient import ApiClient
from skytap.models.SkytapResource import SkytapResource
from skytap.models.UserData import UserData
from skytap.models.Vms import Vms

class Template(SkytapResource):
    """One Skytap template."""

    def __init__(self, tmp_json):
        """Init is mainly handled by the parent class."""
        super(Template, self).__init__(tmp_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Convert the list of VMs into a Vms object group.
        """
        self.data['vms'] = Vms(self.vms, self.url)

    def __getattr__(self, key):
        """Load values for anything that doesn't get loaded by default.

        For user_data, a secondary API call is needed. Only make that
        call when the info is requested.
        """
        if key == 'user_data':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url + '/user_data.json')
            self.user_data = UserData(json.loads(user_json), self.url)
            return self.user_data
        return super(Template, self).__getattr__(key)