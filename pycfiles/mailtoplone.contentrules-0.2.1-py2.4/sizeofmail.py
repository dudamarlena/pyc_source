# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/conditions/sizeofmail.py
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
from mailtoplone.base.interfaces import IEmail
from mailtoplone.contentrules import baseMessageFactory as _

class ISizeOfMailCondition(Interface):
    """Interface for the configurable aspects of a SizeOfMail condition.
    
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__
    operator = schema.Choice(title=_('Relational operator'), description=_('The relational operator to be used'), required=True, values=['>=', '<='], default='>=')
    size = schema.Int(title=_('Size'), description=_('The size to check for in megabytes'), required=True)


class SizeOfMailCondition(SimpleItem):
    """The actual persistent implementation of the SizeOfMail condition.
    
    Note that we must mix in Explicit to keep Zope 2 security happy.
    """
    __module__ = __name__
    implements(ISizeOfMailCondition, IRuleElementData)
    operator = ''
    size = ''
    element = 'mailtoplone.contentrules.conditions.SizeOfMail'

    @property
    def summary(self):
        return _('Check if mail is ${operator} ${size} megabytes', mapping=dict(operator=self.operator, size=self.size))


class SizeOfMailConditionExecutor(object):
    """The executor for this condition.
    
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, ISizeOfMailCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        operator = self.element.operator
        size = self.element.size * 1024 * 1024
        if not IEmail.providedBy(obj):
            return False
        if operator == '>=':
            return len(obj.data) >= size
        if operator == '<=':
            return len(obj.data) <= size
        return False


class SizeOfMailAddForm(AddForm):
    """An add form for SizeOfMail rule conditions.
    """
    __module__ = __name__
    form_fields = form.FormFields(ISizeOfMailCondition)
    label = _('Add SizeOfMail Condition')
    description = _('An SizeOfMail Condition checks the size of a mail (<=, >=) against a user specified size in megabyte')
    form_name = _('Configure element')

    def create(self, data):
        c = SizeOfMailCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class SizeOfMailEditForm(EditForm):
    """An edit form for portal type conditions
    
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(ISizeOfMailCondition)
    label = _('Edit SizeOfMail Condition')
    description = _('An SizeOfMail Condition checks the size of a mail (<=, >=) against a user specified size in megabyte')
    form_name = _('Configure element')