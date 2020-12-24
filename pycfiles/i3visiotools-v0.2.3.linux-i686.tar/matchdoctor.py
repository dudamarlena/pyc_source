# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/matchdoctor.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Matchdoctor(Platform):
    """ 
                A <Platform> object for Matchdoctor.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Matchdoctor'
        self.tags = [
         'contact']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.matchdoctor.com/profile_' + self.NICK_WILDCARD + '.html'
        self.notFoundText = [
         '<title>404 - File or directory not found.</title>']
        self.forbiddenList = []
        self.score = 20.0