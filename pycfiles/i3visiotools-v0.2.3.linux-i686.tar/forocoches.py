# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/forocoches.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform

class Forocoches(Platform):
    """ 
                A <Platform> object for Forocoches.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Forocoches'
        self.tags = [
         'opinions', 'activism']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.forocoches.com/foro/member.php?username=' + self.NICK_WILDCARD
        self.urlEnumeration = 'http://www.forocoches.com/foro/member.php?u=' + '<HERE_GOES_THE_USER_ID>'
        self.notFoundText = [
         'Usuario no registrado, por lo que no tiene un perfil.</div>', '<center>Usuario especificado inv']
        self.forbiddenList = []