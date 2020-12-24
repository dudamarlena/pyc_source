# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/PublicIPs.py
# Compiled at: 2016-12-21 12:50:14
"""Skytap API object wrapping Skytap Public IPs.

This roughly translates to the Skytap API call of /v2/ips REST call,
but gives us better access to the bits and pieces of the VPN.

If accessed via the command line (``python -m skytap.PublicIPs``) this will
return the Public IP info from Skytap in a JSON format.
"""
import sys
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.PublicIP import PublicIP

class PublicIPs(SkytapGroup):
    """Set of Skytap Public IPs.

    Example:
        ips = skytap.PublicIPs()
        print len(ips)
    """

    def __init__(self):
        """Build the IP list from the Skytap API."""
        super(PublicIPs, self).__init__()
        self.load_list_from_api('/v2/ips', PublicIP)


if __name__ == '__main__':
    print PublicIPs().main(sys.argv[1:])