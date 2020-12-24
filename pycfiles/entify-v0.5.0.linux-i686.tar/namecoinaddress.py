# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/patterns/namecoinaddress.py
# Compiled at: 2015-01-05 13:39:33
from entify.lib.patterns.regexp import RegexpObject

class NamecoinAddress(RegexpObject):
    """ 
        <NamecoinAddress> class.
    """

    def __init__(self):
        """ 
            Constructor without parameters.
            Most of the times, this will be the ONLY method needed to be overwritten.

            :param name:    string containing the name of the regular expression.
            :param reg_exp:    string containing the regular expresion.
        """
        self.name = 'i3visio.namecoin.address'
        self.reg_exp = [
         '[^a-zA-Z0-9]' + '([N][a-km-zA-HJ-NP-Z1-9]{26,33})' + '[^a-zA-Z0-9]']