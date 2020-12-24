# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/apps/NewConfigParser.py
# Compiled at: 2017-08-09 04:01:30
import ConfigParser

class NewConfigParser(ConfigParser.ConfigParser):
    """
    Make options keep upper case
    """

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)
        return

    def optionxform(self, optionstr):
        return optionstr