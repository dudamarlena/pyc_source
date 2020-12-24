# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/PublishedServices.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap services."""
from skytap.models.PublishedService import PublishedService
from skytap.models.SkytapGroup import SkytapGroup

class PublishedServices(SkytapGroup):
    """A list of Published Services."""

    def __init__(self, service_json, interface_url):
        """Create the list of Published Services.

        Args:
            services_json (string): The JSON from Skytap API to build the list
                                    from.
        """
        super(PublishedServices, self).__init__()
        self.load_list_from_json(service_json, PublishedService, interface_url)
        for service in self.data:
            self.data[service].data['url'] = interface_url + '/services/' + str(self.data[service].id)