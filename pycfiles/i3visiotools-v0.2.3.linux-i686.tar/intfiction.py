# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/intfiction.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Intfiction(Platform):
    """ 
                A <Platform> object for Intfiction.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Intfiction'
        self.tags = [
         'opinions', 'social']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.intfiction.org/forum/memberlist.php?username=' + self.NICK_WILDCARD
        self.notFoundText = [
         'No members found for this search criterion.']
        self.forbiddenList = ['.']