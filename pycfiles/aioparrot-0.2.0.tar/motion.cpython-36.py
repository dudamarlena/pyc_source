# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/device/motion.py
# Compiled at: 2017-11-22 04:16:51
# Size of source mod 2**32: 167 bytes
from aioouimeaux.device import Device

class Motion(Device):
    device_type = 'Motion'

    def __repr__(self):
        return '<WeMo Motion "{}">'.format(self.name)