# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/ukdebate.py
# Compiled at: 2014-12-25 08:01:31
from platforms import Platform

class Ukdebate(Platform):
    """ 
                A <Platform> object for Ukdebate.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Ukdebate'
        self.tags = [
         'social', 'news']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.ukdebate.co.uk/forums/index.php?action=profile;user=' + self.NICK_WILDCARD
        self.notFoundText = [
         'Grrr, it looks like you are having problems doing something on the UK Debate.']
        self.forbiddenList = ['.']

    def _doesTheUserExist(self, html):
        """ 
                    Method that performs the verification of the existence or not of a given profile. This is a reimplementation of the method found in all the <Platform> objects.     In this case, this will return ALWAYS None because the platform is no longer available.
                        
                        :param html:    The html text in which the self.notFoundText
                        :return :   None if the user was not found in the html text and the html text if the user DOES exist.
                """
        return