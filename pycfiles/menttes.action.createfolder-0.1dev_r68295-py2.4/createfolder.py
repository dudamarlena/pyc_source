# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/menttes/action/createfolder/createfolder.py
# Compiled at: 2008-07-11 18:40:55
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
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

class ICreatefolderAction(Interface):
    """
    Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__
    foldername = schema.TextLine(title=_('Folder'), description='Name of the folder to be created', required=True)


class CreatefolderAction(SimpleItem):
    """The actual persistent implementation of the notify action element.
    """
    __module__ = __name__
    implements(ICreatefolderAction, IRuleElementData)
    foldername = ''
    element = 'menttes.action.createfolder.Createfolder'

    @property
    def summary(self):
        return _('Folder ${foldername}', mapping=dict(foldername=self.foldername))


class CreatefolderActionExecutor(object):
    """The executor for this action.
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, ICreatefolderAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        foldername = self.element.foldername
        normalized = ('-').join(foldername.split(' ')).lower()
        self.event.object.invokeFactory('Folder', title=foldername, id=normalized)
        return True


class CreatefolderAddForm(AddForm):
    """An add form for notify rule actions.
    """
    __module__ = __name__
    form_fields = form.FormFields(ICreatefolderAction)
    label = _('Add Deafult Action')
    description = _('A notify action can show a message to the user.')
    form_name = _('Configure element')

    def create(self, data):
        a = CreatefolderAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class CreatefolderEditForm(EditForm):
    """An edit form for notify rule actions.
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(ICreatefolderAction)
    label = _('Edit Createfolder Action')
    description = _('A createfolder action can show a message to the user.')
    form_name = _('Configure element')