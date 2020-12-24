# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/zrandomlist/__init__.py
# Compiled at: 2018-12-20 12:56:40
import random

def randList():
    """ This method will return a list 
    of 7 random numbers between 1 and 50.
    That's all!!
    """
    return [ random.randint(1, 50) for _ in range(7) ]