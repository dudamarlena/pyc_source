# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lancelot/specs/simple_fns.py
# Compiled at: 2009-02-16 14:47:09
""" Simple functions used in Specs """

def dont_raise_index_error():
    """ Simple fn that does nothing. 
    Aids specifying some behaviours around exceptions """
    pass


def raise_index_error():
    """ Simple fn that raises an index error.
    Aids specifying some behaviours around exceptions """
    raise IndexError('with message')


def number_one():
    """ Simple fn that returns the number One (1). """
    return 1


def string_abc():
    """ Simple fn that returns the string "abc". """
    return 'abc'