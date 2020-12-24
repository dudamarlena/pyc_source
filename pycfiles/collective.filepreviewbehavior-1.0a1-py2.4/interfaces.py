# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/filepreviewbehavior/interfaces.py
# Compiled at: 2010-01-11 09:34:53
from Products import ARFilePreview

class IPreviewable(ARFilePreview.interfaces.IPreviewAware):
    """ Behavior for enabling Products.ARFilePreview support for dexterity
        content types
    """
    __module__ = __name__