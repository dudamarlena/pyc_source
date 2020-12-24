# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\core\interfaces\NetworkInterface.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 780 bytes
import json
from responder3.core.commons import *

class NetworkInterface:

    def __init__(self):
        """
                Container object to describe a network interface
                """
        self.ifname = None
        self.ifindex = None
        self.addresses = []

    def to_dict(self):
        return {'ifname':str(self.ifname), 
         'ifindex':str(self.ifindex), 
         'addresses':self.addresses}

    def to_json(self):
        return json.dumps((self.to_dict()), cls=UniversalEncoder)

    def __repr__(self):
        return str(self)

    def __str__(self):
        t = '== INTERFACE ==\r\n'
        t += 'Name: %s\r\n' % self.ifname
        t += 'ifindex: %s\r\n' % self.ifindex
        for addr in self.addresses:
            t += 'Address: %s\r\n' % str(addr)

        return t