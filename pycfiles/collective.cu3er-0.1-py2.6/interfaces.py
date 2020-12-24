# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/venv26/checkouts/collective.cu3er/collective/cu3er/interfaces.py
# Compiled at: 2010-05-22 15:25:46
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class ICU3ERSpecific(IDefaultPloneLayer):
    """A marker interface that defines a Zope 3 browser layer."""
    pass