# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/oroom.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Oroom(Platform):
    """ 
                A <Platform> object for Oroom.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Oroom'
        self.tags = [
         'opinions', 'activism']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.oroom.org/forum/members/' + self.NICK_WILDCARD
        self.notFoundText = [
         "<title>The Orange Room - Lebanon's number one discussion forums</title>"]
        self.forbiddenList = ['.']