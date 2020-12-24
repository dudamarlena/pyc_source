# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Matrix4x4.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 9496 bytes


class Matrix4x4:
    M: list

    def __init__(self, values):
        if len(values) != 16:
            raise ValueError('There must be sixteen and only sixteen input values for Matrix.')
        self.M = [values[i * 4:i * 4 + 4] for i in range(0, 4)]