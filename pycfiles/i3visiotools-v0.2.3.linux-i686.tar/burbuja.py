# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/burbuja.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Burbuja(Platform):
    """ 
                A <Platform> object for Burbuja.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Burbuja.info'
        self.tags = [
         'opinions', 'activism']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.burbuja.info/inmobiliaria/members/' + self.NICK_WILDCARD + '.html'
        self.notFoundText = [
         'Este usuario no se ha registrado y por lo tanto no tiene un perfil para ver']
        self.forbiddenList = []