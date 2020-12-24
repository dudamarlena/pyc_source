# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/io.py
# Compiled at: 2016-05-27 19:16:13
from raspautomation_cli.device import Device

class IO(Device):
    api_endpoint = 'io'

    def set(self, value):
        self.server.patch('io/%i/dim/' % self.id, data={'state': value})

    def turn_on(self):
        self.server.get('io/%i/on/' % self.id)

    def turn_off(self):
        self.server.get('io/%i/off/' % self.id)

    def toggle(self):
        self.server.get('io/%i/toggle/' % self.id)