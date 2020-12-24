# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/viewlets/google/plusone.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.layer import IZBlogDefaultLayer
from zope.component import adapts
from zope.interface import Interface
from ztfy.skin.viewlet import ContentProviderBase

class GooglePlusOneContentProvider(ContentProviderBase):
    """Google +1 viewlet javascript code"""
    adapts(Interface, IZBlogDefaultLayer, Interface)

    def update(self):
        self.presentation = getattr(self.__parent__, 'presentation', None)
        return

    def render(self):
        if not getattr(self.presentation, 'display_googleplus', False):
            return ''
        return super(GooglePlusOneContentProvider, self).render()