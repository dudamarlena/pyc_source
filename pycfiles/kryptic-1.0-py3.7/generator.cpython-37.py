# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kryptic\generator\generator.py
# Compiled at: 2020-02-20 22:20:07
# Size of source mod 2**32: 2969 bytes
import secrets, string

class Generator(object):
    __doc__ = ' \n    Creates a Generator class that utilizes some RNG source to \n    generate a Pseudo Random Output\n    '

    def __init__(self, source='CryptGenRandom', minlength=6, maxlength=6):
        self.source = source
        self.minlength = max(minlength, 1)
        self.maxlength = max(self.minlength, maxlength)

    def generate(self, minlength=0, maxlength=0, *flags) -> str:
        """
        Generates string with specified parameters (default=all alphanumerics and symbols)
        Flags:
            - c or char:
                generate string using only alphabetic characters
            - a or alphanum:
                generate  string using only alphanumeric characters
            - n or num:
                generate password using only numeric characters
        """
        src = string.printable[:95]
        if 'char' in flags or 'c' in flags:
            src = string.ascii_letters
        else:
            if 'alphanum' in flags or 'a' in flags:
                src = string.printable[:62]
            else:
                if 'num' in flags or 'n' in flags:
                    src = string.digits
        r = len(src)
        if minlength < 1:
            minlength = self.minlength
        if maxlength < 1:
            maxlength = self.maxlength
        output = ''
        for __ in range(self.getRandomLength(minlength, maxlength)):
            num = secrets.SystemRandom(self.source)._randbelow(r)
            output += src[num]

        return output

    def generatePassword(self, minlength=0, maxlength=0, *flags) -> str:
        """
        Generates password string with specified parameters (default=all alphanumerics and symbols)
        Flags:
            - c or char:
                generate string using only alphabetic characters
            - a or alphanum:
                generate  string using only alphanumeric characters
            - n or num:
                generate password using only numeric characters
        """
        return self.generate(minlength, maxlength, flags)

    def generateUsername(self, minlength=0, maxlength=0) -> str:
        """
        Generates an alphanumeric string
        """
        return self.generate(minlength, maxlength, 'a')

    def getRandomLength(self, minlength=0, maxlength=0) -> int:
        """
        Generates a random number between length minlength and maxlength
        """
        if minlength < 1:
            minlength = self.minlength
        if maxlength < 1:
            maxlength = self.maxlength
        if minlength == maxlength:
            return minlength
        return secrets.SystemRandom(self.source)._randbelow(maxlength - minlength) + minlength