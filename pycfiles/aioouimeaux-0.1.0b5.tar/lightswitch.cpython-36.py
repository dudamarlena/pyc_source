# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/device/lightswitch.py
# Compiled at: 2017-11-22 04:40:54
# Size of source mod 2**32: 139 bytes
from .switch import Switch

class LightSwitch(Switch):

    def __repr__(self):
        return '<WeMo LightSwitch "{}">'.format(self.name)