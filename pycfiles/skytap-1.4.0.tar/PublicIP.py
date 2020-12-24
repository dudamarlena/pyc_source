# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/PublicIP.py
# Compiled at: 2016-12-21 13:56:25
"""Support for a Public IP resource in Skytap."""
from skytap.models.SkytapResource import SkytapResource

class PublicIP(SkytapResource):
    """One Public IP service object."""

    def __init__(self, ip_json):
        """Create one PublicIP object."""
        super(PublicIP, self).__init__(ip_json)