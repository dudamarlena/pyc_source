# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/conditions/emailheader.py
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
import email, re
from mailtoplone.base.interfaces import IEmail
from mailtoplone.contentrules import baseMessageFactory as _
from mailtoplone.contentrules.config import vo_headers, vo_headers_default

class IEmailHeaderCondition(Interface):
    """Interface for the configurable aspects of a EmailHeader condition.
    
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__
    header = schema.Choice(title=_('Email Header'), description=_('The Email Header to check for'), required=True, values=vo_headers, default=vo_headers_default)
    value = schema.TextLine(title=_('Value'), description=_('The Value to check for'), required=True)


class EmailHeaderCondition(SimpleItem):
    """The actual persistent implementation of the file extension condition.
    
    Note that we must mix in Explicit to keep Zope 2 security happy.
    """
    __module__ = __name__
    implements(IEmailHeaderCondition, IRuleElementData)
    header = ''
    value = ''
    element = 'mailtoplone.contentrules.conditions.EmailHeader'

    @property
    def summary(self):
        return _('Check ${header} for ${value}', mapping=dict(header=self.header, value=self.value))


class EmailHeaderConditionExecutor(object):
    """The executor for this condition.
    
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IEmailHeaderCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        header = self.element.header
        value = self.element.value
        if not IEmail.providedBy(obj):
            return False
        mailobj = email.message_from_string(obj.data)
        if header not in mailobj.keys():
            return False
        try:
            exp = re.compile(value)
        except:
            return value in mailobj.get(header)

        if re.search(exp, mailobj.get(header)):
            return True
        return False


class EmailHeaderAddForm(AddForm):
    """An add form for EmailHeader rule conditions.
    """
    __module__ = __name__
    form_fields = form.FormFields(IEmailHeaderCondition)
    label = _('Add EmailHeader Condition')
    description = _('An EmailHeader Condition checks a specified header for a specified value, specify value as regular expression')
    form_name = _('Configure element')

    def create(self, data):
        c = EmailHeaderCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class EmailHeaderEditForm(EditForm):
    """An edit form for portal type conditions
    
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(IEmailHeaderCondition)
    label = _('Edit EmailHeader Condition')
    description = _('An EmailHeader Condition checks a specified header for a specified value, value can be a regular expression')
    form_name = _('Configure element')