# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/browser/keywordmapcontrolpanel.py
# Compiled at: 2013-05-08 04:41:18
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Bool
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from redomino.advancedkeyword import _

class IKeywordMapSchema(Interface):
    keywordmapenabled = Bool(title=_('label_keywordmapenabled', default='Enable KeywordMap'), description=_('help_keywordmapenabled', default=''), default=False, required=False)


class KeywordMapControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IKeywordMapSchema)

    def __init__(self, context):
        super(KeywordMapControlPanelAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.advancedkeyword_properties

    keywordmapenabled = ProxyFieldProperty(IKeywordMapSchema['keywordmapenabled'])


class KeywordMapControlPanel(ControlPanelForm):
    form_fields = form.FormFields(IKeywordMapSchema)
    label = _('label_keywordmapsettings', default='KeywordMap settings')
    description = _('help_keywordmapsettings', default='General editing settings.')
    form_name = _('label_keywordmapform', default='AdvancedKeyword settings')