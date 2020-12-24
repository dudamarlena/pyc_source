# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/interfaces.py
# Compiled at: 2010-05-22 11:09:57
__doc__ = ' Interfaces.'
from zope.interface import Interface
__all__ = [
 'IContentProvider']

class IContentProvider(Interface):
    """ Content provider.

    Component of this type provides a piece of content or UI.
    """

    def __call__(context, request):
        """ Provide content."""
        pass