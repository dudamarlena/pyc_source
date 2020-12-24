# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/twitch.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Twitch(Platform):
    """ 
                A <Platform> object for Twitch.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Twitch'
        self.tags = [
         'social', 'video']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.twitch.tv/' + self.NICK_WILDCARD
        self.notFoundText = []
        self.forbiddenList = [
         '.', ' ']

    def _doesTheUserExist(self, html):
        """
                        Method that performs the verification of the existence or not of a given profile. This method may be rewrritten.
                """
        userExistsText = [
         'http://secure.twitch.tv/swflibs/TwitchPlayer.swf?channel=']
        for t in userExistsText:
            if t in html:
                return html

        return