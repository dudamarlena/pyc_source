# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/device/lightswitch.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 148 bytes
from .switch import Switch

class LightSwitch(Switch):

    def __repr__(self):
        return '<WeMo LightSwitch "{name}">'.format(name=(self.name))