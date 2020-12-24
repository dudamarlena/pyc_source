# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyprojecttemplate\demo.py
# Compiled at: 2019-12-15 23:29:34
# Size of source mod 2**32: 245 bytes
from pyprojecttemplate import basicmath
number = 12
print('The square of the number {num} is {num_squared}'.format(num=number, num_squared=(basicmath.calculate_square(number))))