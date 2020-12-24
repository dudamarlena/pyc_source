# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyprojecttemplate\demo.py
# Compiled at: 2019-12-15 23:29:34
# Size of source mod 2**32: 245 bytes
from pyprojecttemplate import basicmath
number = 12
print('The square of the number {num} is {num_squared}'.format(num=number, num_squared=(basicmath.calculate_square(number))))