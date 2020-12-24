# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/italianskin/tool/interfaces.py
# Compiled at: 2009-01-15 04:19:49
from zope.interface import Interface
from zope.schema import List, TextLine
from Products.CMFPlone import PloneMessageFactory as _

class IItalianSkinToolSchema(Interface):
    """ ItalianSkinTool Schema """
    __module__ = __name__
    class_titles = List(title=_('Class titles'), description=_('Your CSS titles'), value_type=TextLine(), required=True)
    css_classes = List(title=_('CSS classes'), description=_('Your CSS classes'), value_type=TextLine(), required=True)


class IItalianSkinTool(IItalianSkinToolSchema):
    """ Marker interface for the ItalianSkin tool """
    __module__ = __name__