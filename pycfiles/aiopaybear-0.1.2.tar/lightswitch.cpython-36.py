# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/device/lightswitch.py
# Compiled at: 2017-11-22 04:40:54
# Size of source mod 2**32: 139 bytes
from .switch import Switch

class LightSwitch(Switch):

    def __repr__(self):
        return '<WeMo LightSwitch "{}">'.format(self.name)