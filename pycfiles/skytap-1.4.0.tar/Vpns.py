# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/Vpns.py
# Compiled at: 2016-12-17 13:32:08
"""Skytap API object wrapping Skytap VPNs.

This roughly translates to the Skytap API call of /v2/vpns REST call,
but gives us better access to the bits and pieces of the VPN.

If accessed via the command line (``python -m skytap.Vpns``) this will
return the VPN information from Skytap in a JSON format.
"""
import sys
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vpn import Vpn

class Vpns(SkytapGroup):
    """Set of Skytap VPNs.

    Example:
        v = skytap.Vpns()
        print len(v)
    """

    def __init__(self):
        """Build the VPN list from the Skytap API."""
        super(Vpns, self).__init__()
        self.load_list_from_api('/v2/vpns', Vpn)


if __name__ == '__main__':
    print Vpns().main(sys.argv[1:])