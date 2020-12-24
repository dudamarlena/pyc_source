# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/autospies.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Autospies(Platform):
    """ 
                A <Platform> object for Askfm.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Autospies'
        self.tags = ['e-commerce', 'opinions']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.autospies.com/users/' + self.NICK_WILDCARD
        self.notFoundText = ['<title>Page not found | Ask.fm</title>']
        self.forbiddenList = ['.']

    def _doesTheUserExist(self, html):
        """ 
                        Method that performs the verification of the existence or not of a given profile. This method may be rewrritten.
                """
        theProfileExists = [
         'View Profile</a>)']
        for t in theProfileExists:
            if t in html:
                return html

        return