# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/browser/configlet.py
# Compiled at: 2010-08-19 05:56:34
"""
configlet.py

Created by Manabu Terada on 2010-08-12.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from zope.component import adapts, queryUtility
from zope.component import getMultiAdapter
from zope.formlib.form import FormFields
from zope.interface import implements
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from c2.app.shorturl.interfaces import IShortUrlSchema
from c2.app.shorturl.interfaces import IShortUrlConfig
from c2.app.shorturl import ShortUrlMessageFactory as _

class ShortUrlControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IShortUrlSchema)

    def getBaseUrl(self):
        util = queryUtility(IShortUrlConfig)
        return getattr(util, 'base_url', '')

    def setBaseUrl(self, value):
        util = queryUtility(IShortUrlConfig)
        if util is not None:
            util.base_url = value
        return

    base_url = property(getBaseUrl, setBaseUrl)

    def getFolderId(self):
        util = queryUtility(IShortUrlConfig)
        data = getattr(util, 'folder_id', None)
        if data is None or not data:
            return ''
        else:
            return data

    def setFolderId(self, value):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        util = queryUtility(IShortUrlConfig)
        if util is not None:
            util.folder_id = value
            if not hasattr(portal, value):
                obj = _createObjectByType('ShortUrlFolder', portal, value, title=value)
                obj.setExcludeFromNav(1)
                obj.reindexObject()
        return

    folder_id = property(getFolderId, setFolderId)


class ShortUrlControlPanel(ControlPanelForm):
    form_fields = FormFields(IShortUrlSchema)
    label = _('ShortUrl settings')
    description = _('Settings to enable and configure queued ShortUrl.')
    form_name = _('ShortUrl settings')