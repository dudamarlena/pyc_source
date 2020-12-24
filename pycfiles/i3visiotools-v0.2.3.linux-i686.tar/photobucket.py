# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/photobucket.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Photobucket(Platform):
    """ 
                A <Platform> object for Photobucket.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Photobucket'
        self.tags = [
         'image']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://smg.photobucket.com/user/' + self.NICK_WILDCARD + '/library/?sort=3&page=1'
        self.notFoundText = [
         '<h2>Sorry, the requested page does not exist.</h2>']
        self.forbiddenList = ['.']