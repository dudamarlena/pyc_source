# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/layer.py
# Compiled at: 2012-06-26 16:42:30
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.layer import IZBlogDefaultLayer, IZBlogDefaultSkin
from zope.schema import TextLine
from ztfy.hplskin import _

class IHPLLayer(IZBlogDefaultLayer):
    """HPL layer - inherited from ZBlog default layer"""
    pass


class IHPLSkin(IZBlogDefaultSkin, IHPLLayer):
    """HPL skin - inherited from ZBlog default skin"""
    label = TextLine(title=_('HPL skin'))