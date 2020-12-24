# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/filepreviewbehavior/interfaces.py
# Compiled at: 2010-01-11 09:34:53
from Products import ARFilePreview

class IPreviewable(ARFilePreview.interfaces.IPreviewAware):
    """ Behavior for enabling Products.ARFilePreview support for dexterity
        content types
    """
    __module__ = __name__