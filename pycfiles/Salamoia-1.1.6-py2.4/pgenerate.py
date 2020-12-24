# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/pgenerate.py
# Compiled at: 2007-12-02 16:26:55
from random import choice, randint
dictionary_file = '/usr/lib/ispell/american.med+'

class Pgenerate:
    """
    This class is a password generator.
    Just inherit it (with optional arguments) and find the password in the class variable 'password'.
    """
    __module__ = __name__

    def __init__(self, min_chars=5, use_dictionary=0):
        self.password = ''
        self.create_password(min_chars, use_dictionary)

    def fetch_word_from_dictionary(self, min_chars):
        """Get a word from a dictionary with minimum [min_chars] characters."""
        word = ''
        words = open(dictionary_file, 'r').readlines()
        while len(word) < min_chars:
            word = choice(words)

        word = word.lower().strip()
        return word

    def warp_password(self):
        """Warps around the chars in the password."""
        warps = {}
        for x in xrange(ord('a'), ord('z') + 1):
            x = chr(x)
            warps[x] = [x, x.upper()]

        specialchars = (
         (
          'a', ['@', '4']), ('e', ['3']), ('g', ['6']), ('i', ['1', '|', '!']), ('l', ['1', '|', '!']), ('o', ['0']), ('s', ['5', 'z', 'Z']), ('t', ['+', '7']), ('z', ['s', 'S', '2']))
        for (a, b) in specialchars:
            warps[a] += b

        randoms = 0
        warped_password = ''
        for i in self.password:
            if i in warps.keys():
                if randint(0, 3):
                    warped_password += choice(warps[i])
                else:
                    warped_password += i
            else:
                warped_password += i

        return warped_password

    def generate_password(self, min_chars):
        """generate_password(min_chars):
Randomly creates a password with minimum [min_chars] length."""
        valid_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        password = ''
        for i in xrange(0, min_chars + randint(0, 2)):
            password += choice(valid_chars)

        return password

    def create_password(self, min_chars, use_dictionary):
        """create_password([min_chars = 4, use_dictionary = 0]):
Either picks a password from a dictionary or generates one randomly, with minimum chars as specified (default 4)."""
        if use_dictionary:
            self.password = self.fetch_word_from_dictionary(min_chars)
        else:
            self.password = self.generate_password(min_chars)
        self.password = self.warp_password()

    def __repr__(self):
        return self.password


from salamoia.tests import *
runDocTests()