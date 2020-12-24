# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: neokami/src/Neokami/Exceptions/NeokamiBlockedException.py
# Compiled at: 2015-04-30 09:52:52
""" Copyright 2015 Neokami GmbH. """
from .NeokamiBaseException import NeokamiBaseException

class NeokamiBlockedException(NeokamiBaseException):
    """raise this when there's a Blocked error"""
    pass