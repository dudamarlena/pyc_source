# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Solgema/solgema/src/Solgema.blinks/Solgema/blinks/interfaces.py
# Compiled at: 2010-08-05 05:16:14
from zope.interface import Interface, Attribute
from plone.theme.interfaces import IDefaultPloneLayer

class ISolgemaBlinksLayer(IDefaultPloneLayer):
    """Solgema portlets manager layer"""
    __module__ = __name__