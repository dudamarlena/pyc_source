# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/layer.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.layer import IZBlogDefaultLayer, IZBlogDefaultSkin
from zope.schema import TextLine
from ztfy.gallery import _

class IGalleryLayer(IZBlogDefaultLayer):
    """Gallery layer - inherited from ZBlog default layer"""
    pass


class IGallerySkin(IZBlogDefaultSkin, IGalleryLayer):
    """Gallery skin - inherited from ZBlog default skin"""
    label = TextLine(title=_('Gallery skin'))