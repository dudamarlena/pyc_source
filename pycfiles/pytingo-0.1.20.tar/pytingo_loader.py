# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/castarco/Proyectos/Pytingo/pytingo/pytingo_loader.py
# Compiled at: 2014-06-15 14:10:35
from __future__ import absolute_import, division, print_function, unicode_literals

class PytingoLoader:
    """
    Settings Loader. Abstract class.
    """

    def __init__(self):
        pass

    def get(self, section):
        """
        """
        raise NotImplementedError()