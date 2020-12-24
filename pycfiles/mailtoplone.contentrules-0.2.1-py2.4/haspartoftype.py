# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/conditions/haspartoftype.py
# Compiled at: 2008-02-29 08:26:12
__author__ = 'Hans-Peter Locher<hans-peter.locher@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 36831 $'
__version__ = '$Revision: 1.7 $'[11:-2]
from persistent import Persistent
from OFS.SimpleItem import SimpleItem
from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
import email
from mailtoplone.base.interfaces import IEmail
from mailtoplone.contentrules import baseMessageFactory as _

class IHasPartOfTypeCondition(Interface):
    """Interface for the configurable aspects of a HasPartOfType condition.
    
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__
    maintype = schema.TextLine(title=_('Maintype'), description=_('The maintype to check for'), required=False)
    subtype = schema.TextLine(title=_('Subtype'), description=_('The subtype to check for'), required=False)


class HasPartOfTypeCondition(SimpleItem):
    """The actual persistent implementation of the HasPartOfType condition.
    
    Note that we must mix in Explicit to keep Zope 2 security happy.
    """
    __module__ = __name__
    implements(IHasPartOfTypeCondition, IRuleElementData)
    maintype = ''
    subtype = ''
    element = 'mailtoplone.contentrules.conditions.HasPartOfType'

    @property
    def summary(self):
        return _('Check if the email contains a part with maintype/subtype pair ${maintype}/${subtype}', mapping=dict(maintype=self.maintype, subtype=self.subtype))


class HasPartOfTypeConditionExecutor(object):
    """The executor for this condition.
    
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IHasPartOfTypeCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        maintype = self.element.maintype
        subtype = self.element.subtype
        if not IEmail.providedBy(obj):
            return False
        mailobj = email.message_from_string(obj.data)
        for part in mailobj.walk():
            if maintype and subtype:
                pass
            else:
                if part.get_content_maintype() == maintype:
                    if part.get_content_subtype() == subtype:
                        return True
                if maintype and not subtype:
                    if part.get_content_maintype() == maintype:
                        return True
                if not maintype and subtype:
                    if part.get_content_subtype() == subtype:
                        return True
                if not maintype and not subtype:
                    return True

        return False


class HasPartOfTypeAddForm(AddForm):
    """An add form for HasPartOfType rule conditions.
    """
    __module__ = __name__
    form_fields = form.FormFields(IHasPartOfTypeCondition)
    label = _('Add HasPartOfType Condition')
    description = _('A HasPartOfType Condition checks if the email contains a part of specified maintype/subtype')
    form_name = _('Configure element')

    def create(self, data):
        c = HasPartOfTypeCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class HasPartOfTypeEditForm(EditForm):
    """An edit form for portal type conditions
    
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(IHasPartOfTypeCondition)
    label = _('Edit HasPartOfType Condition')
    description = _('A HasPartOfType Condition checks if the email contains a part of specified maintype/subtype')
    form_name = _('Configure element')