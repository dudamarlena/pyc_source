# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/enumerite.py
# Compiled at: 2007-12-02 16:26:58


def enumerite(arg, base=1):
    """
    like enumerate() but starts counting from
    an arbitrary number (defaults 1)
    """
    for (c, i) in enumerate(arg):
        yield (
         c + base, i)


def enumboolate(arg, start=True):
    """
    takes [a,b,c,...] and returns [(1,a),(0,b),(1,c),...]
    useful in: for high, i in enumbolite(objects): ....
    for alternated patterns of things
    """
    for (c, i) in enumerate(arg):
        yield (
         start ^ c % 2, i)


from salamoia.tests import *
runDocTests()