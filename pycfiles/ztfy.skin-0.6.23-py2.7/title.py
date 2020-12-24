# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/viewlets/header/title.py
# Compiled at: 2013-02-09 09:13:40
__docformat__ = 'restructuredtext'
from zope.dublincore.interfaces import IZopeDublinCore
from zope.traversing.api import getName
from ztfy.skin.viewlet import ViewletBase

class TitleViewlet(ViewletBase):
    """Title viewlet"""

    @property
    def title(self):
        try:
            title = self.__parent__.title
        except AttributeError:
            title = getattr(self.context, 'title', None)
            if title is None:
                dc = IZopeDublinCore(self.context, None)
                if dc is not None:
                    title = dc.title

        if not title:
            title = '[ %s ]' % getName(self.context)
        return title