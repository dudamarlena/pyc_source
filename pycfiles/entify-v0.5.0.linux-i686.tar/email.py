# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/patterns/email.py
# Compiled at: 2015-01-05 13:39:33
from entify.lib.patterns.regexp import RegexpObject

class Email(RegexpObject):
    """ 
                <Email> class. It identifies emails that include:
                    foo@bar.com
                    foo[at]bar[dot]com
                    foo[arroba]bar[punto]com
                    foo [at] bar [dot] com
        """

    def __init__(self):
        """ 
                        Constructor without parameters.
                        Most of the times, this will be the ONLY method needed to be overwritten.

                        :param name:    string containing the name of the regular expression.
                        :param reg_exp: string containing the regular expresion.
                """
        self.name = 'i3visio.email'
        self.reg_exp = [
         '([a-zA-Z0-9\\.\\-_]+(?:@| ?\\[(?:arroba|at)\\] ?)[a-zA-Z0-9\\.\\-]+(?:\\.| ?\\[(?:punto|dot)\\] ?)[a-zA-Z]+)']