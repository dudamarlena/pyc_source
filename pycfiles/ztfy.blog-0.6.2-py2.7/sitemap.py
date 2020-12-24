# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/sitemap.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.interfaces import IContainerSitemapInfo
from ztfy.skin.page import BaseTemplateBasedPage

class SiteManagerMapsIndexView(BaseTemplateBasedPage):
    """Site manager sitemaps index view"""
    pass


def getValues(parent, context, output):
    output.append(context)
    contents = IContainerSitemapInfo(context, None)
    if contents is not None:
        for item in contents.values:
            getValues(context, item, output)

    return


class SiteManagerSitemapView(BaseTemplateBasedPage):
    """Site manager sitemap view"""

    def getContents(self):
        result = []
        getValues(None, self.context, result)
        return result