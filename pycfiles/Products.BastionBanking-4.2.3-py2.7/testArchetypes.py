# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/tests/testArchetypes.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl
from Acquisition import aq_base
from Products.BastionBanking.ZCurrency import ZCurrency
from Products.BastionBanking.Archetypes import AmountField, AmountWidget
from Products.BastionBanking.config import PROJECTNAME
from Products.Archetypes.atapi import registerType, BaseContent, Schema
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFTestCase.ctc import setupCMFSite
try:
    from Products.Archetypes.tests.attestcase import ATTestCase
except KeyError:
    from Products.PloneTestCase.PloneTestCase import PloneTestCase as ATTestCase

from Products.Archetypes.tests.utils import PACKAGE_HOME
from Products.Archetypes.tests.utils import makeContent

class Dummy(BaseContent):
    schema = BaseContent.schema.copy() + Schema((
     AmountField('amount', required=False, searchable=True, write_permission=ModifyPortalContent, widget=AmountWidget(description='Currency Amount', description_msgid='help_value', label='Economic Value', label_msgid='label_Value', i18n_domain='plone')),))
    meta_type = portal_type = archetype_name = 'Dummy'
    immediate_view = 'base'
    default_view = 'base'


AccessControl.class_init.InitializeClass(Dummy)
registerType(Dummy, PROJECTNAME)

class TestArchetypes(ATTestCase):
    """Tests our Archetypes widgets - well actually its completely broken because
    we somehow need to installProduct our little dummy class so as we can
    create objects..."""

    def XtestTest(self):
        """
        hmmm - do widget tests *really* work???   NO!!!!
        """
        self.loginAsPortalOwner()
        self.portal.createObject(type_name='Dummy', id='doc')
        doc = self.portal.doc
        field = doc.Schema()['amount']
        widget = field.widget
        form = {'amount': 'USD 1.23'}
        expected = ZCurrency('USD 1.23')
        result = widget.process_form(doc, field, form)

    def XtestRendering(self):
        self.loginAsPortalOwner()
        self.portal.createObject(type_name='Dummy', id='doc')
        doc = self.portal.doc
        view = doc.base_view()
        edit = doc.base_edit()


from unittest import TestSuite, makeSuite

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestArchetypes))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')