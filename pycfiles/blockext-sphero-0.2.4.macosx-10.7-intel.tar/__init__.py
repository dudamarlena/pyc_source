# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/blockext_sphero/__init__.py
# Compiled at: 2014-08-15 18:05:32
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
from blockext import *
import sphero
__version__ = b'0.2.4'

class Sphero:

    def __init__(self):
        self.robot = sphero.Sphero()
        self.robot.connect()
        self.robot.set_back_led_output(255)
        self.name = self.robot.get_bluetooth_info().name

    def _problem(self):
        if not self.robot:
            return b'Your Sphero is not connected'

    def _on_reset(self):
        self.robot.roll(0, 0)

    def get_sphero_name(self):
        return self.name

    def set_sphero_name(self, name):
        self.name = name
        self.robot.set_device_name(name)

    def roll_sphero(self, power, heading):
        self.robot.roll(power * 2.55, heading)

    def set_sphero_color(self, r, g, b):
        self.robot.set_rgb(r, g, b)


descriptor = Descriptor(name=b'Orbotix Sphero', port=7575, blocks=[
 Block(b'roll_sphero', b'command', b'roll Sphero %n percent speed at %n degrees', defaults=[100, 0]),
 Block(b'get_sphero_name', b'reporter', b'get Sphero name'),
 Block(b'set_sphero_name', b'command', b'set Sphero name to %s', defaults=[b'Rob Orb']),
 Block(b'set_sphero_color', b'command', b'set Sphero color to R: %n G: %n B: %n')])
extension = Extension(Sphero, descriptor)
if __name__ == b'__main__':
    extension.run_forever(debug=True)