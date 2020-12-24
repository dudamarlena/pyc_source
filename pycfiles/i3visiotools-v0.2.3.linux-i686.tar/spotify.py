# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/spotify.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Spotify(Platform):
    """ 
                A <Platform> object for Spotify.
        """

    def __init__(self):
        """  
                        Constructor... 
                """
        self.platformName = 'Spotify'
        self.tags = ['social', 'music']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://open.spotify.com/user/' + self.NICK_WILDCARD
        self.forbiddenList = [
         ' ']

    def _doesTheUserExist(self, html):
        """ 
                        Method that performs the verification of the existence or not of a given profile. This method has been rewritten as the standard notFoundText approach is not possible and we have to look for text that appears on VALID profiles.
                """
        userExistsText = [
         '<h3>Top Tracks</h3>']
        for t in userExistsText:
            if t in html:
                return html

        return