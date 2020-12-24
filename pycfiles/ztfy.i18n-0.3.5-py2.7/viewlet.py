# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/viewlet.py
# Compiled at: 2013-02-04 05:24:18
__docformat__ = 'restructuredtext'
from z3c.language.switch.interfaces import II18n
from ztfy.skin.viewlets.header.title import TitleViewlet

class I18nTitleViewlet(TitleViewlet):
    """I18n title viewlet"""

    @property
    def title(self):
        try:
            title = self.__parent__.title
        except AttributeError:
            title = II18n(self.context, None).queryAttribute('title', request=self.request)

        return title