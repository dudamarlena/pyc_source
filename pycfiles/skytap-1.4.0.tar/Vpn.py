# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Vpn.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap VPNs."""
from skytap.models.SkytapResource import SkytapResource

class Vpn(SkytapResource):
    """One Skytap VPN object."""

    def __init__(self, vpn_json):
        """Create one VPN object."""
        super(Vpn, self).__init__(vpn_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Create an 'active' flag based on the status of the VPN.
        """
        self.active = self.status == 'active'