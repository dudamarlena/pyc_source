# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/profiles.py
# Compiled at: 2011-06-08 07:37:53
import configobj, os

class Configuration(object):

    def __init__(self):
        self.home_config = os.path.join(os.path.expanduser('~'), '.joy2mouse')
        if not os.path.exists(self.home_config):
            with open(self.home_config, 'w') as (fh):
                fh.write(DEFAULT)
        self.config = configobj.ConfigObj(self.home_config)


DEFAULT = "# Default joystick device to read from\ndevice = /dev/input/js0\n# In order to speed up or slow down the mouse movements, change this field\n# the higher the value, the slower the pointer!\ndivisor = 20000\n\n[Example]\naxis = 0 1\n0 = mouse 1\n1 = mouse 2\n4 = mouse 4\n5 = mouse 5\n\n[Minecraft]\n# Profile's device will overwrite the default device\ndevice = /dev/input/js0\n# Profile's divisor will overwrite the default divisor\ndivisor = 15000\naxis = 0 1 4 5 \n0 = mouse 1\n1 = mouse 2\n2 = w\n3 = space\n4 = mouse 4\n5 = mouse 5\n"
config = Configuration()