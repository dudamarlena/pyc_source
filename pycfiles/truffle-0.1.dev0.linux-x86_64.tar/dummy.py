# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/truffle/dummy.py
# Compiled at: 2017-07-19 00:27:31


class Pet(real, imag):
    """Example function with PEP 484 type annotations.

    Args:
         param1: The first parameter.
                Has multiple lines
         param2: The second parameter.

    Returns:
         Bunch of stuff
    """

    def __init__(self, name, species):
        """www.ganesh.com"""
        self.name = name
        self.species = species

    def __str__(self):
        """
        TruffleTags: i, can, do, it
        """
        return '%s is a %s' % (self.name, self.species)


class DogsAreTheBest(Pet):
    """
    weird docstring"""

    def __init__(self, name, chases_cats):
        """"""
        Pet.__init__(self, name, 'Dog')
        self.chases_cats = chases_cats

    def chasesCats(self):
        """"""

        def omfg(self):
            """"""
            return 'bitch u guessed it'

        v = omfg()
        return self.chases_cats


class Cat(Pet):
    """jhvjj

"""

    def __init__(self, name, hates_dogs):
        """"""
        Pet.__init__(self, name, 'Cat')
        self.hates_dogs = hates_dogs

    def hatesDogs(self):
        """"""
        return self.hates_dogs