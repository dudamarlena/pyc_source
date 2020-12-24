# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/dashboard.py
# Compiled at: 2010-09-26 21:54:06
import pprint
from copy import deepcopy
from zope.interface import implements
from Products.Archetypes.public import *
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from anz.dashboard.config import PROJECTNAME
from anz.dashboard.interfaces import IDashboard
from anz.dashboard import MSG_FACTORY as _
DashboardSchema = ATContentTypeSchema.copy() + Schema((StringField('config', widget=TextAreaWidget(lable='Config', description=_('debug only. do not touch this if you do not know detail about it.'), visible={'edit': 'invisible', 'view': 'invisible'}, size=20)), StringField('pageLayout', default='tile', vocabulary=DisplayList((('tile', _('page_layout_tile', default='Tile mode')), ('tab', _('page_layout_tab', default='Tab mode')))), widget=SelectionWidget(label=_('label_page_layout_mode', default='Page layout mode'), description=_('help_page_layout_mode', default="            You can choose 'tile mode' or\n\t\t\t'tab mode'. With 'tile mode', all pages are shown in one page, from\n\t\t\ttop to bottom, it is useful for you to make very complex composite\n\t\t\tpage. With 'tab mode', you can switch pages using the top tab\n\t\t\tlinks."), i18n_domain='anz.dashboard'))))

class Dashboard(ATCTContent):
    """ Dashboard is a content type to build composite page. """
    __module__ = __name__
    implements(IDashboard)
    schema = DashboardSchema
    portal_type = meta_type = 'Anz Dashboard'
    archetype_name = 'Anz Dashboard'
    defaultPageConfig = {'columns': [], 'title': 'untitled page', 'width': '100%'}
    defaultColumnConfig = {'width': '0.5', 'style': 'padding:5px 0 5px 5px', 'widgets': []}
    defaultWidgetCfg = {'id': '', 'color': '', 'style': '', 'collapse': 0, 'options': {'title': 'Un-titled widget'}}

    def __init__(self, oid, **kw):
        super(Dashboard, self).__init__(oid, **kw)
        self._layoutCfg = []
        self._layoutCfg.append(deepcopy(self.defaultPageConfig))
        self._layoutCfg[0]['columns'].append(deepcopy(self.defaultColumnConfig))
        self._layoutCfg[0]['columns'].append(deepcopy(self.defaultColumnConfig))
        self._p_changed = True

    def getConfig(self, retStr=True):
        """ """
        return retStr and pprint.pformat(self._layoutCfg) or self._layoutCfg

    def setConfig(self, value):
        if value:
            value = value.replace('\n', ' ').replace('\r', '')
            self._layoutCfg = eval(value)


registerType(Dashboard, PROJECTNAME)