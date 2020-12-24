# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/mcneel.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Mcneel(Platform):
    """ 
                A <Platform> object for Mcneel.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Mcneel'
        self.tags = [
         'professional']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://discourse.mcneel.com/users/' + self.NICK_WILDCARD
        self.notFoundText = [
         '>The page you requested doesn&#39;t exist or is private.</h1>']
        self.forbiddenList = ['.']
        self.score = 10.0