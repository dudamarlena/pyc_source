# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/browser/expires_form.py
# Compiled at: 2008-09-16 09:06:59
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
import datetime
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.formlib.form import action
from plone.fieldsets.fieldsets import FormFieldsets
from plone.fieldsets.form import FieldsetsEditForm
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from redomino.autodelete.interfaces import IExpires
from redomino.autodelete.interfaces import IExpiresExtendedSchema
from redomino.autodelete.interfaces import IExpirable
from redomino.autodelete import autodeleteMessageFactory as _

class ExpiresExtendedSchema(SchemaAdapterBase):
    """ Extends the schema of IExpires and provides more methods to set the delete_date provided by IExpires """
    __module__ = __name__
    adapts(IExpirable)
    implements(IExpiresExtendedSchema)

    def __init__(self, context):
        super(ExpiresExtendedSchema, self).__init__(context)
        self.context = context

    def get_relative_days(self):
        now = datetime.datetime.now()
        adapted = IExpires(self.context, None)
        delete_date = adapted.delete_date
        days = 0
        if delete_date:
            delta = delete_date - now
            days = delta.days + 1
            if days < 0:
                days = 0
        else:
            return days
        return days

    def set_relative_days(self, value):
        if value:
            delta = datetime.timedelta(days=value)
            today = datetime.datetime.today()
            delete_date = today + delta
            adapted = IExpires(self.context, None)
            adapted.delete_date = delete_date
        return

    relative_days = property(get_relative_days, set_relative_days)


class FieldsetsEditFormMixin(FieldsetsEditForm):
    """ Mixin class with a fieldset template """
    __module__ = __name__
    template = ViewPageTemplateFile('templates/fieldset.pt')


relativedate_set = FormFieldsets(IExpiresExtendedSchema)
relativedate_set.id = 'days'
relativedate_set.label = _('Days of validity')

class ExpiresForm(FieldsetsEditFormMixin):
    """ Edit annotations form """
    __module__ = __name__
    form_fields = FormFieldsets(relativedate_set)
    label = _('Autodelete form settings')
    description = _('Here you can choose either an absolute delete date or a number of days of validity for this item.')
    form_name = _('Expires form settings')

    @property
    def delete_date(self):
        adapted = IExpires(self.context, None)
        delete_date = adapted.delete_date
        return delete_date


class EnableExpiresCondition(BrowserView):
    """Returns True or False depending on whether the enable expires action is allowed
    on current context.
    """
    __module__ = __name__

    @property
    def _action_condition(self):
        context = self.context
        return not IExpirable.providedBy(context) and not IPloneSiteRoot.providedBy(context)

    def __call__(self):
        return self._action_condition


class DisableExpiresCondition(BrowserView):
    """Returns True or False depending on whether the disable expires action is allowed
    on current context.
    """
    __module__ = __name__

    @property
    def _action_condition(self):
        return IExpirable.providedBy(self.context)

    def __call__(self):
        return self._action_condition


class EnableExpiresForm(PageForm):
    """ Enable expiration form (autodelete) """
    __module__ = __name__
    form_fields = []
    label = _('Enable expires (autodelete)')
    description = _('This object once expired will be deleted')
    form_name = _('Enable expires form (autodelete)')

    @action(_('Enable autodelete'))
    def enable(self, action, data):
        context = self.context
        alsoProvides(context, IExpirable)
        adapted = IExpires(context, None)
        adapted._reindex()
        status_message = _('Enabled autodelete for this item')
        url = getMultiAdapter((context, self.request), name='absolute_url')()
        IStatusMessage(self.request).addStatusMessage(_(status_message), type='info')
        self.request.response.redirect(url)
        return ''


class DisableExpiresForm(PageForm):
    """ Disable expiration form (autodelete) """
    __module__ = __name__
    form_fields = []
    label = _('Disable autodelete')
    description = _('Turn off the delete_date expiration')
    form_name = _('Disable expires form (autodelete)')

    @action(_('Disable autodelete'))
    def disable(self, action, data):
        context = self.context
        noLongerProvides(context, IExpirable)
        adapted = IExpires(context, None)
        adapted.flush()
        status_message = _('Disabled autodelete for this item')
        url = getMultiAdapter((context, self.request), name='absolute_url')()
        IStatusMessage(self.request).addStatusMessage(_(status_message), type='info')
        self.request.response.redirect(url)
        return ''