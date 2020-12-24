# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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