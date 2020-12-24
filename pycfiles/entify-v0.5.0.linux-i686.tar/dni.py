# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/patterns/dni.py
# Compiled at: 2015-01-05 13:39:33
from entify.lib.patterns.regexp import RegexpObject

class DNI(RegexpObject):
    """ 
        <DNI> class.
    """

    def __init__(self):
        """ 
            Constructor without parameters.
            Most of the times, this will be the ONLY method needed to be overwritten.

            :param name:    string containing the name of the regular expression.
            :param reg_exp:    string containing the regular expresion.
        """
        self.name = 'i3visio.dni'
        self.reg_exp = [
         '[^a-zA-Z1-9]' + '[0-9]{7,8}[\\-\\ ]?[a-zA-Z]' + '[^a-zA-Z1-9]']

    def isValidExp(self, exp):
        """     
            Method to verify if a given expression is correct just in case the used regular expression needs additional processing to verify this fact.$
            This method will be overwritten when necessary.

            :param exp:     Expression to verify.

            :return:        True | False
        """
        order = [
         'T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E', 'T']
        l = exp[(len(exp) - 1)]
        try:
            number = int(exp[0:7])
        except:
            try:
                number = int(exp[0:6])
            except:
                pass

        if l == order[(number % 23)]:
            return True
        else:
            return False