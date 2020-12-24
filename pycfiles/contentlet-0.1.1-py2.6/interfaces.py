# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/interfaces.py
# Compiled at: 2010-05-22 11:09:57
""" Interfaces."""
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