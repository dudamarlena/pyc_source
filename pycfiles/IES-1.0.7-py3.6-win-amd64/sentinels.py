# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\sentinels.py
# Compiled at: 2018-01-15 22:34:11
# Size of source mod 2**32: 205 bytes
from strategycontainer.utils.sentinel import sentinel
NotSpecified = sentinel('NotSpecified', 'Singleton sentinel value used for Term defaults.')
NotSpecifiedType = type(NotSpecified)