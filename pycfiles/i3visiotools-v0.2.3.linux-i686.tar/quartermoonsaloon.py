# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/quartermoonsaloon.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Quartermoonsaloon(Platform):
    """ 
                A <Platform> object for Quartermoonsaloon.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Quartermoonsaloon'
        self.tags = [
         'opinions', 'activism']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://quartermoonsaloon.com/forum/member.php?username=' + self.NICK_WILDCARD
        self.notFoundText = [
         'This user has not registered and therefore does not have a profile to view.']
        self.forbiddenList = ['.']