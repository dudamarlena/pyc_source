# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/menu.py
# Compiled at: 2013-03-15 02:58:19
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.layer import IZBlogDefaultSkin
from ztfy.skin.menu import SkinTargetMenuItem, SkinTargetJsMenuItem, SkinTargetDialogMenuItem

class DefaultSkinMenuItem(SkinTargetMenuItem):
    """Customized menu item for ZBlog skin targets"""
    skin = IZBlogDefaultSkin


class DefaultSkinJsMenuItem(SkinTargetJsMenuItem):
    """Customized JS menu item for ZBlog skin targets"""
    skin = IZBlogDefaultSkin


class DefaultSkinDialogMenuItem(SkinTargetDialogMenuItem):
    """Customized dialog menu item for ZBlog skin targets"""
    skin = IZBlogDefaultSkin