# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/analytics.py
# Compiled at: 2017-07-07 17:23:19
from lxml.html import builder as html_builder
from lxml.html import fragments_fromstring as html_fromstring
from lxml.html import tostring as html_tostring
from plone.app.layout.analytics.view import AnalyticsViewlet as AnalyticsViewletBase
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

class AnalyticsViewlet(AnalyticsViewletBase):

    def render(self):
        """render the webstats snippet adding a div arround it
        """
        ptool = getToolByName(self.context, 'portal_properties')
        snippet = safe_unicode(ptool.site_properties.webstats_js)
        div = html_builder.DIV({'id': 'plone-analytics'})
        tags = html_fromstring(snippet)
        div.extend(tags)
        snippet = safe_unicode(html_tostring(div))
        return snippet