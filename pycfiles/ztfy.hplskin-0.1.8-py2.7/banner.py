# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/viewlets/header/banner.py
# Compiled at: 2013-09-22 11:04:15
__docformat__ = 'restructuredtext'
import random
from z3c.language.switch.interfaces import II18n
from ztfy.base.interfaces import IBaseContent
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.hplskin.interfaces import IBannerManager
from zope.component import queryAdapter
from ztfy.skin.viewlet import ViewletBase
from ztfy.utils.traversing import getParent

class BannerViewlet(ViewletBase):

    @property
    def langs(self):
        content = getParent(self.context, IBaseContent, allow_context=True)
        return II18n(content).getAvailableLanguages()

    @property
    def banner(self):
        site = getParent(self.context, ISiteManager)
        banner = queryAdapter(site, IBannerManager, 'top')
        if banner:
            return random.choice(banner.values())
        else:
            return