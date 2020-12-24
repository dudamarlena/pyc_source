# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/italianskin/tool/utils/action_utils.py
# Compiled at: 2009-01-15 04:19:49
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
from Products.CMFCore.utils import getToolByName

def install_actions(self):
    ai = getToolByName(self, 'portal_actionicons')
    try:
        ai.getActionIcon('plone', 'validateXhtml')
    except KeyError:
        ai.addActionIcon('plone', 'validateXhtml', 'ItalianSkinValidation.gif', 'Validate XHTML code')

    pa = getToolByName(self, 'portal_actions')
    try:
        pa.getActionInfo('document_actions/validateXhtml')
    except ValueError:
        pa.addAction('validateXhtml', name='Validate XHTML code', action='string:${object_url}/validate_xhtml_form', condition='python: object.portal_type in ["Document", "News", "Event"]', permission='View', category='document_actions')


def uninstall_actions(self):
    ai = getToolByName(self, 'portal_actionicons')
    try:
        ai.removeActionIcon('plone', 'validateXhtml')
    except:
        pass

    pa = getToolByName(self, 'portal_actions')
    acts = list(pa.listActions())
    selection_indexes = [ acts.index(a) for a in acts if a.id == 'validateXhtml' ]
    pa.deleteActions(selection_indexes)