# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/qPloneDropDownMenu/utils.py
# Compiled at: 2010-07-19 08:14:01
__doc__ = ' Utility functions '
from zope.component import getMultiAdapter
from OFS.DTMLMethod import addDTMLMethod
from Products.CMFCore.utils import getToolByName
try:
    from plone.app.upgrade.utils import safeEditProperty
except:
    from Products.CMFPlone.migrations.migration_util import safeEditProperty

from Products.CMFCore.Expression import Expression, createExprContext
from config import PROPERTY_FIELD, PROPERTY_SHEET
TAB_HTML_SNIPPET = '<li id="portaltab-%(id)s" class="plain">\n  <a href="%(url)s" accesskey="t" title="%(desc)s">%(name)s</a>\n</li>\n'

def addCSS(container, sheetId, title, csshovering):
    """ Add DTML Method object to portal root """
    addDTMLMethod(container, sheetId, title, csshovering)


def updateMenu(site):
    pu = getToolByName(site, 'plone_utils')
    pa = getToolByName(site, 'portal_actions')
    portal_props = getToolByName(site, 'portal_properties')
    context_state = getMultiAdapter((site, site.REQUEST), name='plone_context_state')
    actions = context_state.actions()
    if type(actions) == dict:
        actions = actions['portal_tabs']
    portal_tabs_view = getMultiAdapter((site, site.REQUEST), name='portal_tabs_view')
    portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)
    value = ''
    enc = portal_props.site_properties.getProperty('default_charset', 'utf-8')
    for tab in portal_tabs:
        value += TAB_HTML_SNIPPET % {'id': toUnicode(tab['id'], enc), 'url': toUnicode(tab['url'], enc), 
           'desc': toUnicode(tab['description'], enc), 
           'name': toUnicode(tab['name'], enc)}

    if not hasattr(portal_props.aq_base, PROPERTY_SHEET):
        portal_props.addPropertySheet(PROPERTY_SHEET, 'DropDown Menu Properties')
    ap = getattr(portal_props.aq_base, PROPERTY_SHEET)
    safeEditProperty(ap, PROPERTY_FIELD, value, 'text')


def toUnicode(value, enc='utf-8'):
    if isinstance(value, str):
        return value.decode(enc)
    else:
        return value