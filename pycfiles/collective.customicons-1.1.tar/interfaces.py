# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/venv26/checkouts/collective.cu3er/collective/cu3er/interfaces.py
# Compiled at: 2010-05-22 15:25:46
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class ICU3ERSpecific(IDefaultPloneLayer):
    """A marker interface that defines a Zope 3 browser layer."""