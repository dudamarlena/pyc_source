# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/freerepublic.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Freerepublic(Platform):
    """ 
                A <Platform> object for Freerepublic.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Freerepublic'
        self.tags = [
         'activism']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.freerepublic.com/~' + self.NICK_WILDCARD
        self.notFoundText = [
         '<title>Error</title>']
        self.forbiddenList = ['.']
        self.score = 10.0