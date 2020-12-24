# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/reflex/browser/form.py
# Compiled at: 2019-11-07 04:23:37
import logging
from collective.reflex import _
from collective.reflex.interfaces import IReportIssue
from collective.reflex.interfaces import IReportIssueList
from collective.reflex.interfaces import IStateTransition
from collective.reflex.interfaces import IStateTransitionList
from collective.reflex.utils import get_state
from collective.z3cform.datagridfield import DataGridFieldFactory
from plone import api
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.lifecycleevent import modified
from zope.schema import getFieldNamesInOrder
logger = logging.getLogger(__name__)

class StateTransitionForm(form.EditForm):
    """Report State Transition"""
    _schema = IStateTransition
    _finished = False
    label = _('Report State Transition')
    prefix = 'form.state.transition'
    fields = field.Fields(IStateTransitionList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = [
     'steps', 'portal_type', 'sample_id', 'barcode',
     'name', 'project_type', 'submission_company',
     'report_state', 'detection_plan']

    def __init__(self, context, request):
        super(StateTransitionForm, self).__init__(context, request)
        self.request['disable_border'] = True
        self.items = []

    def datagridInitialise(self, subform, widget):
        """This is called when the subform fields have been initialised,
        but before the widgets have been created.
        Field based configuration could occur here.
        """
        pass

    def getContent(self):
        """
        Return the content to be displayed and/or edited.
        DATA = {
            'batch_list': [
                   {'sample_id': 'Big Office Block',
                    'barcode': 'My Office',
                    'name': 'The Old Sod',
                    },
                   {'sample_id': 'Easy Street',
                    'barcode': 'Home Sweet Home',
                    'name': 'The Old Sod',
                    }
            ]}
        """
        data = {'batch_list': []}
        names = getFieldNamesInOrder(self._schema)
        for obj in self.items:
            record = {}
            for name in names:
                record[name] = getattr(obj, name, None)

            record['uuid'] = obj.UID()
            record['review_state'] = api.content.get_state(obj)
            if 'report_state' in names:
                record['report_state'] = translate(_(get_state(obj).title()), context=api.portal.getRequest())
            data['batch_list'].append(record)

        return data

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        edit_count = 0
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            if obj:
                transition = entry['transition_state']
                change_note = entry['changeNote']
                if transition:
                    api.content.transition(obj=obj, transition=transition, comment=change_note)
                    edit_count += 1

        if edit_count:
            api.portal.show_message(_('${count} Item state changed', mapping={'count': edit_count}), self.request, 'info')
            logger.info(('{count} item state changed.').format(count=edit_count))
        return edit_count

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.report_state = self.formErrorsMessage
            return
        else:
            count = self.dumpOutput(data)
            if count is not None:
                self._finished = True
            return

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(_('operation cancelled'), self.request, 'info')
        self.request.response.redirect(self.nextURL())

    def update(self):
        """get some data init

        # self._schema.omit('sample_id')
        # self._schema['sample_id'].readonly=True
        # assert len(uuids) > 0
        """
        uuids = self.request.get('uuids', '')
        uuids = uuids and uuids.split(',') or []
        for uuid in uuids:
            item = api.content.uuidToObject(uuid)
            review_state = api.content.get_state(item)
            if item and review_state == 'success':
                self.items.append(item)

        super(StateTransitionForm, self).update()

    def updateActions(self):
        """Bypass the baseclass editform - it causes problems"""
        super(form.EditForm, self).updateActions()

    def updateWidgets(self, prefix=None):
        super(StateTransitionForm, self).updateWidgets()
        self.widgets['batch_list'].auto_append = False
        self.widgets['batch_list'].allow_reorder = False
        self.widgets['batch_list'].allow_insert = False
        self.widgets['batch_list'].allow_delete = False
        self.widgets['batch_list'].columns[0]['mode'] = HIDDEN_MODE

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """This is called when the subform widgets have been created.
        At this point, you can configure the widgets,
        e.g. specify the size of a widget.
        """
        if 'uuid' in widgets:
            widgets['uuid'].mode = HIDDEN_MODE
        for name in self.fields_readonly:
            if name in widgets:
                widgets[name].mode = DISPLAY_MODE

    @property
    def action(self):
        """See interfaces.IInputForm"""
        self._parent_action = super(StateTransitionForm, self).action
        parent_url = self.context.absolute_url()
        view_name = self.__name__
        return parent_url + '/' + view_name

    def nextURL(self):
        url = self.context.absolute_url()
        return url

    def render(self):
        if self._finished:
            self.request.response.redirect(self.nextURL())
            return ''
        return super(StateTransitionForm, self).render()


class ReportIssueForm(StateTransitionForm):
    """"""
    label = _('Report Issue')
    _schema = IReportIssue
    fields = field.Fields(IReportIssueList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory

    def getContent(self):
        data = {'batch_list': []}
        names = getFieldNamesInOrder(self._schema)
        warn_count = 0
        for obj in self.items:
            record = {}
            if get_state(obj) != 'reviewed':
                warn_count += 1
                continue
            for name in names:
                record[name] = getattr(obj, name, None)

            record['uuid'] = obj.UID()
            record['review_state'] = api.content.get_state(obj)
            if 'report_state' in names:
                record['report_state'] = translate(_(get_state(obj).title()), context=api.portal.getRequest())
            data['batch_list'].append(record)

        if warn_count:
            api.portal.show_message(_('${count} item cannot be manipulated', mapping={'count': warn_count}), self.request, 'warn')
        return data

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        edit_count = 0
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            if obj:
                transition = 'issue'
                change_note = entry['changeNote']
                if transition:
                    api.content.transition(obj=obj, transition=transition, comment=change_note)
                    edit_count += 1
                template_name = entry['template_name']
                self.request.form['template_name'] = template_name
                create = getMultiAdapter((
                 obj, self.request), name='collective-create-report')
                create()
                modified(obj)

        if edit_count:
            api.portal.show_message(_('${count} reports have been issued', mapping={'count': edit_count}), self.request, 'info')
            logger.info(('{count} reports have been issued').format(count=edit_count))
        return edit_count