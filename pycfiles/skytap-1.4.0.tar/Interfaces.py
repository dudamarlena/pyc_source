# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Interfaces.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap interfacess."""
from skytap.models.Interface import Interface
from skytap.models.SkytapGroup import SkytapGroup

class Interfaces(SkytapGroup):
    """A list of Interfaces."""

    def __init__(self, interface_json, vm_url):
        """Create the list of Interfaces.

        Args:
            interfaces_json (string): The JSON from Skytap API to build
                                      the list from.
        """
        super(Interfaces, self).__init__()
        self.load_list_from_json(interface_json, Interface, vm_url)
        for i in self.data:
            self.data[i].data['url'] = vm_url + '/interfaces/' + str(self.data[i].id)