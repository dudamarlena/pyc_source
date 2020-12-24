# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/viewlets/header/sections.py
# Compiled at: 2013-03-09 05:34:56
__docformat__ = 'restructuredtext'
import copy
from zope.publisher.interfaces.browser import IBrowserSkinType
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.skin.interfaces import IDefaultView
from zope.component import queryMultiAdapter, queryUtility
from zope.publisher.browser import applySkin
from zope.traversing.api import getParents
from ztfy.jqueryui import jquery_alerts
from ztfy.skin.viewlet import ViewletBase
from ztfy.utils.request import setRequestData
from ztfy.utils.traversing import getParent

class SectionsListViewlet(ViewletBase):

    def update(self):
        super(SectionsListViewlet, self).update()
        jquery_alerts.need()

    @property
    def sections(self):
        site = getParent(self.context, ISiteManager, allow_context=True)
        if site is not None:
            parents = getParents(self.context) + [self.context]
            for section in site.getVisibleContents():
                selected = section in parents
                if selected:
                    setRequestData('ztfy.blog.section.selected', section, self.request)
                yield {'section': section, 'selected': selected}

        return

    @property
    def manage_url(self):
        skin = queryUtility(IBrowserSkinType, 'ZTFY.BO')
        if skin is not None:
            fake = copy.copy(self.request)
            applySkin(fake, skin)
        else:
            fake = self.request
        adapter = queryMultiAdapter((self.context, fake, self.__parent__), IDefaultView)
        if adapter is not None:
            return adapter.getAbsoluteURL()
        else:
            return