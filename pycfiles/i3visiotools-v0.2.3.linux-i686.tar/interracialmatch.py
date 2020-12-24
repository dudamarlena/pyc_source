# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/interracialmatch.py
# Compiled at: 2014-12-25 08:01:31
from platforms import Platform

class Interracialmatch(Platform):
    """ 
                A <Platform> object for Interracialmatch.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Interracialmatch'
        self.tags = [
         'contact']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.interracialmatch.com/user?' + self.NICK_WILDCARD
        self.notFoundText = [
         'InterracialMatch.com - #1 Dating Site for Interracial Singles']
        self.forbiddenList = ['.']
        self.score = 10.0

    def _doesTheUserExist(self, html):
        """ 
                    Method that performs the verification of the existence or not of a given profile. This is a reimplementation of the method found in all the <Platform> objects.     In this case, this will return ALWAYS None because the platform is no longer available.
                        
                        :param html:    The html text in which the self.notFoundText
                        :return :   None if the user was not found in the html text and the html text if the user DOES exist.
                """
        return