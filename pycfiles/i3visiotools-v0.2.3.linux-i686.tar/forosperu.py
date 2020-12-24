# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/forosperu.py
# Compiled at: 2014-12-25 08:01:31
from platforms import Platform

class Forosperu(Platform):
    """ 
                A <Platform> object for Forosperu.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Forosperu'
        self.tags = [
         'opinions']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.forosperu.net/member.php?username=' + self.NICK_WILDCARD
        self.notFoundText = [
         '>Este usuario no se ha registrado y por lo tanto no tiene un perfil para ver.</div>']
        self.forbiddenList = ['.']

    def _doesTheUserExist(self, html):
        """ 
                    Method that performs the verification of the existence or not of a given profile. This is a reimplementation of the method found in all the <Platform> objects.     In this case, this will return ALWAYS None because the platform is no longer available.
                        
                        :param html:    The html text in which the self.notFoundText
                        :return :   None if the user was not found in the html text and the html text if the user DOES exist.
                """
        return