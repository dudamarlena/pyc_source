# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/client.py
# Compiled at: 2015-11-11 06:54:58
"""
ucloud python sdk client.
"""
from api import umon, unet, uhost, udisk
from utils import base

class Client(object):
    """
    ucloud python sdk client.
    """

    def __init__(self, base_url, public_key, private_key, debug=False, timing=False):
        self.base_url = base_url
        self.private_key = private_key
        self.public_key = public_key
        self.uhost = uhost.UhostManager(self)
        self.unet = unet.UnetManager(self)
        self.umon = umon.UmonManager(self)
        self.udisk = udisk.UdiskManager(self)
        self.client = base.HTTPClient(base_url, debug, timing)

    def get_timing(self):
        return self.client.get_timing()

    def reset_timing(self):
        self.client.reset_timing()