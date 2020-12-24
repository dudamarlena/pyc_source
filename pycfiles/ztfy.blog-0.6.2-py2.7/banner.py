# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/viewlets/header/banner.py
# Compiled at: 2014-05-08 12:30:11
__docformat__ = 'restructuredtext'
from z3c.language.switch.interfaces import II18n
from ztfy.blog.interfaces import IBaseContent
from ztfy.i18n.interfaces.content import II18nBaseContent
from ztfy.skin.viewlet import ViewletBase
from ztfy.utils.traversing import getParent

class BannerViewlet(ViewletBase):

    @property
    def langs(self):
        content = getParent(self.context, II18nBaseContent, allow_context=True)
        if content is None:
            return ()
        else:
            return II18n(content).getAvailableLanguages()

    @property
    def banner(self):
        content = getParent(self.context, IBaseContent, allow_context=True)
        while content is not None:
            i18n = II18n(content, None)
            if i18n is not None:
                image = i18n.queryAttribute('header', request=self.request)
                if image is not None:
                    return image
            content = getParent(content, IBaseContent, allow_context=False)

        return