# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/customizablePersonalizeForm/browser/interfaces.py
# Compiled at: 2011-09-08 04:35:46
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope browser layer.
    """


class IPersonalizeFormValidators(Interface):
    """An simple interface to implement validators
    """