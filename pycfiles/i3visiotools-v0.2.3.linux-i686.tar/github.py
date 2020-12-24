# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/github.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Github(Platform):
    """ 
                A <SocialNetwork> object for Github.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Github'
        self.tags = ['development']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'https://github.com/' + self.NICK_WILDCARD
        self.notFoundText = ['This is not the web page you are looking for']
        self.forbiddenList = []