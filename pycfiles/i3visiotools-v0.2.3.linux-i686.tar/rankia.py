# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/rankia.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Rankia(Platform):
    """ 
                A <Platform> object for Rankia.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Rankia'
        self.tags = [
         'contact', 'professional']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.rankia.com/usuarios/' + self.NICK_WILDCARD
        self.notFoundText = [
         '<title>La página que estás buscando no existe (404)</title>']
        self.forbiddenList = ['.']