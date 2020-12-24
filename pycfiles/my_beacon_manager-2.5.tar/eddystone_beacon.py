# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rajatg/pyProjects/beacons/beacons/portal/models/eddystone_beacon.py
# Compiled at: 2015-12-28 04:13:17
import base64
from beacons import Beacon

class EddyStone(Beacon):
    """
    Eddystone beacon protocol
    """

    def advertised_id(self):
        """
        Convert namespace+instance into advertised id
        """
        beacon_id = self.namespace + self.instance
        beacon_id = int(beacon_id, 16)
        return base64.b64encode(self.long_to_bytes(beacon_id))

    def __init__(self, form):
        super(self.__class__, self).__init__(form)
        self.namespace = form.get('namespace')
        self.instance = form.get('instance')