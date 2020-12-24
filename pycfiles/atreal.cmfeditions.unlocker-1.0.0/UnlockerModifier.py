# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.cmfeditions.unlocker/atreal/cmfeditions/unlocker/UnlockerModifier.py
# Compiled at: 2011-11-16 03:48:53
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.permissions import ManagePortal
from Products.CMFEditions.interfaces.IModifier import ISaveRetrieveModifier
from Products.CMFEditions.interfaces.IModifier import IConditionalTalesModifier
from Products.CMFEditions.Modifiers import ConditionalTalesModifier

def initialize(context):
    """Registers modifiers with zope (on zope startup).
    """
    for m in modifiers:
        context.registerClass(m['wrapper'], m['id'], permission=ManagePortal, constructors=(
         m['form'], m['factory']), icon=m['icon'])


def install(portal_modifier):
    """Registers modifiers in the modifier registry (at tool install time).
    """
    try:
        import plone.app.upgrade
        providedBy = IConditionalTalesModifier.providedBy
    except ImportError:
        providedBy = IConditionalTalesModifier.isImplementedBy

    for m in modifiers:
        id = m['id']
        if id in portal_modifier.objectIds():
            continue
        title = m['title']
        modifier = m['modifier']()
        wrapper = m['wrapper'](id, modifier, title)
        enabled = m['enabled']
        if providedBy(wrapper):
            wrapper.edit(enabled, m['condition'])
        else:
            wrapper.edit(enabled)
        portal_modifier.register(m['id'], wrapper)


manage_UnlockerModifierAddForm = PageTemplateFile('www/UnlockerModifierAddForm.pt', globals(), __name__='manage_UnlockerModifierAddForm')

def manage_addUnlockerModifier(self, id, title=None, REQUEST=None):
    """Add a External Editor modifier
    """
    modifier = UnlockerModifier()
    self._setObject(id, ConditionalTalesModifier(id, modifier, title))
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')
    return


class UnlockerModifier:
    """ 
    """
    __implements__ = (
     ISaveRetrieveModifier,)

    def beforeSaveModifier(self, obj, clone):
        clone.__dict__['_dav_writelocks'] = None
        return ({}, [], [])

    def afterRetrieveModifier(self, obj, repo_clone, preserve=()):
        return ([], [], {})


InitializeClass(UnlockerModifier)
modifiers = (
 {'id': 'UnlockerModifier', 
    'title': 'Unlock the clone before saving it', 
    'enabled': True, 
    'condition': 'python: True', 
    'wrapper': ConditionalTalesModifier, 
    'modifier': UnlockerModifier, 
    'form': manage_UnlockerModifierAddForm, 
    'factory': manage_addUnlockerModifier, 
    'icon': 'www/modifier.gif'},)