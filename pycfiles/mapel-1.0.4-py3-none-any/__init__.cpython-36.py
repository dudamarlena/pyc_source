# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/Snochacz/Documents/GitHub/mapel\mapel\__init__.py
# Compiled at: 2020-03-11 16:37:10
# Size of source mod 2**32: 211 bytes
from .voting import modern as mo

def test():
    print('Welcome to Mapel!')


def print_2d(name):
    mo.print_2d(name)


def print_matrix(name, scale=1.0):
    mo.generate_matrix(name, scale)