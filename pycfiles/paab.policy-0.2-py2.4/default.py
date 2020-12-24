# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paab/policy/actions/default.py
# Compiled at: 2008-03-09 13:46:41
from OFS.SimpleItem import SimpleItem
from persistent import Persistent
from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone import PloneMessageFactory
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.browser.formhelper import AddForm, EditForm

class IDefaultAction(Interface):
    """
    Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__


class DefaultAction(SimpleItem):
    """The actual persistent implementation of the notify action element.
    """
    __module__ = __name__
    implements(IDefaultAction, IRuleElementData)
    element = 'paab.policy.Default'

    @property
    def summary(self):
        pass


class DefaultActionExecutor(object):
    """The executor for this action.
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IDefaultAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        obj = self.event.object
        parent = obj.getParentNode()
        r = parent.title
        if obj.Subject() == ():
            obj.setSubject(r)
            obj.reindexObject()
        return True


class DefaultAddForm(AddForm):
    """An add form for notify rule actions.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDefaultAction)
    label = _('Add Deafult Action')
    description = _('A notify action can show a message to the user.')
    form_name = _('Configure element')

    def create(self, data):
        a = DefaultAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class DefaultEditForm(EditForm):
    """An edit form for notify rule actions.
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDefaultAction)
    label = _('Edit Default Action')
    description = _('A default action can show a message to the user.')
    form_name = _('Configure element')