# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/actions/deliver.py
# Compiled at: 2008-02-29 08:26:12
__author__ = 'Hans-Peter Locher<hans-peter.locher@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 36831 $'
__version__ = '$Revision: 1.7 $'[11:-2]
from OFS.SimpleItem import SimpleItem
from persistent import Persistent
from zope.interface import implements, Interface
from zope.component import adapts, getUtility
from zope.formlib import form
from zope import schema
import OFS.subscribers
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
import transaction
from Acquisition import aq_inner, aq_parent, aq_base
from ZODB.POSException import ConflictError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from mailtoplone.base.interfaces import IMailDropBoxFactory, IMailDropBox
from mailtoplone.contentrules import baseMessageFactory as _

class IDeliverAction(Interface):
    """Interface for the configurable aspects of a deliver action.
    
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__
    key = schema.TextLine(title=_('Key'), description=_('Key used to determine the DropBox'), required=True)


class DeliverAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    __module__ = __name__
    implements(IDeliverAction, IRuleElementData)
    key = ''
    element = 'mailtoplone.contentrules.actions.deliver'

    @property
    def summary(self):
        return _('Deliver to DropBoxes by key ${key}', mapping=dict(key=self.key))


class DeliverActionExecutor(object):
    """The executor for this action.
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IDeliverAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        parent = aq_parent(aq_inner(obj))
        key = self.element.key
        dropbox_factory = getUtility(IMailDropBoxFactory)
        dropboxes = dropbox_factory(obj, key)
        for dropbox in dropboxes:
            if dropbox is not parent:
                IMailDropBox(dropbox).drop(obj.data)

        return True


class DeliverAddForm(AddForm):
    """An add form for deliver actions.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDeliverAction)
    label = _('Add Deliver Action')
    description = _('A deliver action can drop an email to (a) different inbox(es).')
    form_name = _('Configure element')

    def create(self, data):
        a = DeliverAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class DeliverEditForm(EditForm):
    """An edit form for deliver rule actions.
    
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDeliverAction)
    label = _('Edit Deliver Action')
    description = _('A deliver action can drop an email to (a) different inbox(es).')
    form_name = _('Configure element')