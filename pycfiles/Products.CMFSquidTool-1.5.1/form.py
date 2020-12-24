# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/Products/CMFResource/browser/form.py
# Compiled at: 2018-05-16 18:23:05
import logging
from datetime import datetime
from Products.CMFResource import _
from Products.CMFResource.interfaces import IReportAudit
from Products.CMFResource.interfaces import IReportAuditList
from collective.z3cform.datagridfield import DataGridFieldFactory
from plone import api
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.lifecycleevent import modified
from zope.schema import getFieldNamesInOrder
logger = logging.getLogger(__name__)

class ReportAuditEditForm(form.EditForm):
    _schema = IReportAudit
    _finished = False
    label = _('Report Audit')
    prefix = 'form.report.audit'
    fields = field.Fields(IReportAuditList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = [
     'steps', 'portal_type', 'sample_no', 'barcode',
     'name', 'sample_source', 'submission_hospital',
     'detection_plan']

    def __init__(self, context, request):
        super(ReportAuditEditForm, self).__init__(context, request)
        self.request['disable_border'] = True
        self.items = []

    def datagridInitialise(self, subform, widget):
        pass

    def getContent(self):
        data = {'batch_list': []}
        names = getFieldNamesInOrder(self._schema)
        for obj in self.items:
            record = {}
            for name in names:
                record[name] = getattr(obj, name, None)

            record['uuid'] = obj.UID()
            record['review_state'] = api.content.get_state(obj)
            data['batch_list'].append(record)

        return data

    def dumpOutput(self, data):
        """
        """
        batch_list = data.get('batch_list', [])
        edit_count = 0
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            change_note = entry['changeNote']
            if obj:
                old_report_state = obj.report_state
                new_report_state = entry['report_state']
                if old_report_state != new_report_state:
                    if new_report_state == 'audited':
                        report_time = getattr(obj, 'report_time', None)
                        if not report_time:
                            setattr(obj, 'report_time', datetime.now())
                        template_name = entry['template_name']
                        self.request.form['template_name'] = template_name
                        create = getMultiAdapter((
                         obj, self.request), name='pccreate-report')
                        create()
                    change_note = ('{0} - {1}->{2}: {3}.').format(translate(self.label, context=api.portal.getRequest()), translate(_(old_report_state), context=api.portal.getRequest()), translate(_(new_report_state), context=api.portal.getRequest()), change_note if change_note else '')
                    annotation = IAnnotations(self.context.REQUEST)
                    annotation['plone.app.versioningbehavior' + '-changeNote'] = change_note
                    obj.report_state = new_report_state
                    modified(obj)
                    edit_count += 1

        if edit_count:
            api.portal.show_message(_('${count} item(s) have been audited.', mapping={'count': edit_count}), self.request, 'info')
            logger.info(('{count} item(s) have been audited.').format(count=edit_count))
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
        uuids = self.request.get('uuids', '')
        uuids = uuids and uuids.split(',') or []
        for uuid in uuids:
            item = api.content.uuidToObject(uuid)
            review_state = api.content.get_state(item)
            if item and review_state == 'success':
                self.items.append(item)

        super(ReportAuditEditForm, self).update()

    def updateActions(self):
        super(form.EditForm, self).updateActions()

    def updateWidgets(self, prefix=None):
        super(ReportAuditEditForm, self).updateWidgets()
        self.widgets['batch_list'].auto_append = False
        self.widgets['batch_list'].allow_reorder = False
        self.widgets['batch_list'].allow_insert = False
        self.widgets['batch_list'].allow_delete = False
        self.widgets['batch_list'].columns[0]['mode'] = HIDDEN_MODE

    def datagridUpdateWidgets(self, subform, widgets, widget):
        if 'uuid' in widgets:
            widgets['uuid'].mode = HIDDEN_MODE
        for name in self.fields_readonly:
            if name in widgets:
                widgets[name].mode = DISPLAY_MODE

    @property
    def action(self):
        self._parent_action = super(ReportAuditEditForm, self).action
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
        return super(ReportAuditEditForm, self).render()