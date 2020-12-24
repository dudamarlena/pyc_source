# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/zentyal.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Zentyal(Platform):
    """ 
                A <Platform> object for Zentyal.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Zentyal'
        self.tags = [
         'opinions', 'professional', 'development']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'https://forum.zentyal.org/index.php?action=profile;user=' + self.NICK_WILDCARD
        self.notFoundText = [
         'The user whose profile you are trying to view does not exist.']
        self.forbiddenList = ['.']