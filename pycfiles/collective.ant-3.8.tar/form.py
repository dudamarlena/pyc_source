# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/ant/browser/form.py
# Compiled at: 2019-12-07 06:34:28
import logging
from itertools import count
from Acquisition import IAcquirer
from Acquisition import aq_base
from Acquisition import aq_inner
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.ant import _
from collective.ant import utils
from collective.ant.events import StepsChangedEvent
from collective.ant.interfaces import IChangeSteps, ISample
from collective.ant.interfaces import IChangeStepsList
from collective.ant.interfaces import IFailedRedo
from collective.ant.interfaces import IFailedRedoList
from collective.ant.interfaces import IResultList
from collective.ant.interfaces import ISampleList
from collective.ant.interfaces import IStateTransition
from collective.ant.interfaces import IStateTransitionList
from collective.ant.utils import make_folder
from collective.ant.utils import set_recent_group
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContentInContainer
from plone.uuid.interfaces import IUUIDGenerator
from z3c.form import form, field, button
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import NOT_CHANGED
from zope.annotation import IAnnotations
from zope.component import createObject
from zope.component import getUtility
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import modified
from zope.schema import getFieldNamesInOrder
from zope.schema import getFieldsInOrder
logger = logging.getLogger(__name__)

def applyChanges(form, content, data):
    changes = {}
    for name, field_ in form.fields.items():
        try:
            newValue = data[name]
        except KeyError:
            continue

        if newValue is NOT_CHANGED:
            continue
        if field_.field.readonly:
            continue
        setattr(content, field_.__name__, newValue)
        changes.setdefault(field_.field.interface, []).append(name)

    return changes


class SingleSampleAddForm(form.AddForm):
    """add single  form
    https://docs.plone.org/external/plone.app.dexterity/
    docs/advanced/custom-add-and-edit-forms.html
    """
    utils = NotImplemented
    label = _('Single Sample')
    prefix = 'form.single.sample.add'
    success_message = _('Item created')
    fields = field.Fields(ISample)

    def __init__(self, context, request):
        super(SingleSampleAddForm, self).__init__(context, request)
        self.portal_type = self.utils.portal_type

    def create(self, data):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = createObject(fti.factory)
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        applyChanges(self, content, data)
        return aq_base(content)

    def add(self, object):
        container = make_folder(self.aq_parent)
        new_object = addContentToContainer(container, object)

    def nextURL(self):
        parent_url = self.context.absolute_url()
        view_name = self.__name__
        return parent_url + '/' + view_name

    def backURL(self):
        return self.context.absolute_url()

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            obj = self.createAndAdd(data)
            if obj is not None:
                self._finishedAdd = True
                api.portal.show_message(self.success_message, self.request, 'info')
            return

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(_('operation cancelled'), self.request, 'info')
        self.request.response.redirect(self.backURL())


class BaseSingleAddForm(SingleSampleAddForm):
    """"""
    utils = utils
    fields = field.Fields(ISample)


class SampleAddForm(form.AddForm):
    """Subclass overloading: ISampleList"""
    utils = NotImplemented
    fields = field.Fields(ISampleList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory

    def __init__(self, context, request):
        super(SampleAddForm, self).__init__(context, request)
        self.portal_type = self.utils.portal_type
        self.steps_group = self.utils.steps_group
        self.request['disable_border'] = True
        self.items = []
        view_name_fragment = self.__name__.split('-')
        self.prefix = ('.').join(view_name_fragment)
        self.step_name = view_name_fragment[(-2)]
        if self.step_name in self.steps_group:
            self.label = self.steps_group[self.step_name]['title']
            self.form_schema = self.steps_group[self.step_name]['interface']

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
        return data

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        add_count = 0
        gid = getUtility(IUUIDGenerator)()
        container = make_folder(self.aq_parent)
        fields = dict((field_tuple[0], field_tuple[1]) for field_tuple in getFieldsInOrder(self.form_schema) if field_tuple[1].readonly is False)
        'uuid' in fields and fields.pop('uuid')
        for entry in batch_list:
            field_data = {key:val for key, val in entry.items() if key in fields}
            obj = createContentInContainer(container, portal_type=self.portal_type, gid=gid, steps=self.step_name, **field_data)
            add_count += 1

        if add_count:
            set_recent_group(self.portal_type, gid)
        api.portal.show_message(_('${count} Item created', mapping={'count': add_count}), self.request, 'info')
        logger.info(('{count} item(s) added successfully.').format(count=add_count))
        return add_count

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            count = self.dumpOutput(data)
            context = self.getContent()
            for k, v in data.items():
                context[k] = v

            if count is not None:
                self._finishedAdd = True
            return

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(_('operation cancelled'), self.request, 'info')
        self.request.response.redirect(self.nextURL())

    def updateActions(self):
        """Bypass the baseclass editform - it causes problems"""
        super(form.AddForm, self).updateActions()

    def updateWidgets(self, prefix=None):
        super(SampleAddForm, self).updateWidgets()
        self.widgets['batch_list'].auto_append = False
        self.widgets['batch_list'].allow_reorder = True
        self.widgets['batch_list'].allow_insert = True
        self.widgets['batch_list'].allow_delete = True
        self.widgets['batch_list'].columns[0]['mode'] = HIDDEN_MODE

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """This is called when the subform widgets have been created.
        At this point, you can configure the widgets,
        e.g. specify the size of a widget.
        """
        widgets['uuid'].mode = HIDDEN_MODE

    @property
    def action(self):
        """See interfaces.IInputForm"""
        parent_url = self.context.absolute_url()
        view_name = self.__name__
        return parent_url + '/' + view_name

    def nextURL(self):
        url = self.context.absolute_url()
        return url

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ''
        return super(SampleAddForm, self).render()


class SampleEditForm(form.EditForm):
    """"""
    utils = NotImplemented
    fields = field.Fields(ISampleList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = []
    fields_readmask = []
    _finishedAdd = False
    _add_view = False
    _edit_view = False

    def __init__(self, context, request):
        super(SampleEditForm, self).__init__(context, request)
        self.portal_type = self.utils.portal_type
        self.steps_group = self.utils.steps_group
        self.request['disable_border'] = True
        self.items = []
        view_name_fragment = self.__name__.split('-')
        self.prefix = ('.').join(view_name_fragment)
        self.check_step = None
        self.fields_readonly.extend(self.fields_readmask)
        self.step_name = view_name_fragment[(-2)]
        if self.step_name in self.steps_group:
            self.label = self.steps_group[self.step_name]['title']
            self.form_schema = self.steps_group[self.step_name]['interface']
            steps_keys = self.steps_group.keys()
            step_index = steps_keys.index(self.step_name)
            if view_name_fragment[(-1)].startswith('add'):
                self._add_view = True
                self.check_step = steps_keys[(step_index - 1)]
            elif view_name_fragment[(-1)].startswith('edit'):
                self._edit_view = True
                self.check_step = self.step_name
        return

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
        names = getFieldNamesInOrder(self.form_schema)
        for obj in self.items:
            record = {}
            for name in names:
                record[name] = getattr(obj, name, None)
                if record[name] and name in self.fields_readmask:
                    record[name] = '***'

            record['uuid'] = obj.UID()
            if 'review_state' in names:
                record['review_state'] = translate(_(api.content.get_state(obj).title()), context=api.portal.getRequest())
            data['batch_list'].append(record)

        return data

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        add_count = 0
        edit_count = 0
        fields = dict((field_tuple[0], field_tuple[1]) for field_tuple in getFieldsInOrder(self.form_schema) if field_tuple[1].readonly is False)
        'uuid' in fields and fields.pop('uuid')
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            if obj:
                edit_count += 1
                [ setattr(obj, key, val) for key, val in entry.items() if key in fields
                ]
                if self._add_view:
                    old_steps = obj.steps
                    obj.steps = self.step_name
                    notify(StepsChangedEvent(obj, old_steps, self.step_name))
                modified(obj)

        if add_count:
            api.portal.show_message(_('${count} Item created', mapping={'count': add_count}), self.request, 'info')
            logger.info(('{count} item(s) added successfully.').format(count=add_count))
        if edit_count:
            api.portal.show_message(_('${count} Item edited', mapping={'count': edit_count}), self.request, 'info')
            msg = ('{count} item(s) edited successfully.').format(count=edit_count)
            logger.info(msg)
        return add_count or edit_count

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            count = self.dumpOutput(data)
            if count is not None:
                self._finishedAdd = True
            return

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(_('operation cancelled'), self.request, 'info')
        self.request.response.redirect(self.nextURL())

    def update(self):
        """get some data init

        # self.form_schema.omit('sample_id')
        # self.form_schema['sample_id'].readonly=True
        # assert len(uuids) > 0
        """
        uuids = self.request.get('uuids', '')
        uuids = uuids and uuids.split(',') or []
        query = {'UID': {'query': uuids, 'operator': 'or'}}
        results = api.content.find(**query)
        warn_count = 0
        for item in results:
            item = item.getObject()
            if self.check_step:
                if item and item.steps == self.check_step:
                    self.items.append(item)
                else:
                    warn_count += 1
            else:
                self.items.append(item)

        if warn_count:
            api.portal.show_message(_('${count} item cannot be manipulated', mapping={'count': warn_count}), self.request, 'warn')
        super(SampleEditForm, self).update()

    def updateActions(self):
        """Bypass the baseclass editform - it causes problems"""
        super(form.EditForm, self).updateActions()

    def updateWidgets(self, prefix=None):
        super(SampleEditForm, self).updateWidgets()
        self.widgets['batch_list'].auto_append = False
        self.widgets['batch_list'].allow_insert = False
        self.widgets['batch_list'].allow_reorder = True
        self.widgets['batch_list'].columns[0]['mode'] = HIDDEN_MODE
        if not self._add_view:
            self.widgets['batch_list'].allow_reorder = False
            self.widgets['batch_list'].allow_insert = False
            self.widgets['batch_list'].allow_delete = False
            self.widgets['batch_list'].auto_append = False

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """This is called when the subform widgets have been created.
        At this point, you can configure the widgets,
        e.g. specify the size of a widget.
        """
        widgets['uuid'].mode = HIDDEN_MODE
        for name in self.fields_readonly:
            if name in widgets:
                widgets[name].mode = DISPLAY_MODE

    @property
    def action(self):
        """See interfaces.IInputForm"""
        parent_url = self.context.absolute_url()
        view_name = self.__name__
        return parent_url + '/' + view_name

    def nextURL(self):
        url = self.context.absolute_url()
        return url

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ''
        return super(SampleEditForm, self).render()


class BaseEditForm(SampleEditForm):
    """"""
    utils = utils
    fields = field.Fields(IResultList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = ['sample_id', 'barcode']


class FailedRedoEditForm(BaseEditForm):
    """"""
    utils = utils
    fields = field.Fields(IFailedRedoList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = ['sample_id', 'barcode', 'name', 'review_state']
    form_schema = IFailedRedo
    label = _('Failed redo')
    _finishedAdd = False

    def getContent(self):
        data = {'batch_list': []}
        names = getFieldNamesInOrder(self.form_schema)
        warn_count = 0
        for obj in self.items:
            if api.content.get_state(obj=obj) != 'failed':
                warn_count += 1
                continue
            record = {}
            for name in names:
                record[name] = getattr(obj, name, None)

            record['uuid'] = obj.UID()
            record['review_state'] = translate(_(api.content.get_state(obj).title()), context=api.portal.getRequest())
            data['batch_list'].append(record)

        if warn_count:
            api.portal.show_message(_('${count} item cannot be manipulated', mapping={'count': warn_count}), self.request, 'warn')
        return data

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        add_count = 0
        steps_keys = self.steps_group.keys()
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            if obj:
                change_note = entry['changeNote']
                redo_step_name = entry['steps']
                step_index = steps_keys.index(redo_step_name)
                if step_index < 1:
                    continue
                new_step = steps_keys[(step_index - 1)]
                copy_name = set()
                for key in steps_keys[:step_index]:
                    step_schema = self.steps_group[key]['interface']
                    fields_name = self.utils.get_fields_name(step_schema)[1:]
                    copy_name.update(fields_name)

                copy_name.update(['gid', 'creation_date', 'title'])
                container = obj.aq_parent
                new_obj = createContentInContainer(container, portal_type=self.portal_type)
                [ setattr(new_obj, name, getattr(obj, name, '')) for name in copy_name
                ]
                new_obj.sample_id = self.get_unique_sampleno(obj.sample_id)
                new_obj.barcode = self.get_unique_barcode(obj.barcode)
                new_obj.steps = new_step
                add_count += 1
                change_note = ('{title} {step}: {note}').format(title=translate(self.label, context=api.portal.getRequest()), step=translate(_(self.steps_group[redo_step_name]['title']), context=api.portal.getRequest()), note=change_note if change_note else '')
                annotation = IAnnotations(self.context.REQUEST)
                annotation['plone.app.versioningbehavior-changeNote'] = change_note
                modified(new_obj)

        if add_count:
            api.portal.show_message(_('${count} Item created', mapping={'count': add_count}), self.request, 'info')
            logger.info(('{count} item added successfully.').format(count=add_count))
        return add_count

    def get_unique_sampleno(self, sampleno):
        pair = sampleno.split('-')
        start = 1
        if len(pair) == 2:
            try:
                start = int(pair[(-1)]) + 1
            except ValueError:
                pair[0] = sampleno

        new_sampleno = ('{0}-{0}').format(pair[0])
        for n in count(start):
            new_sampleno = ('{0}-{1}').format(pair[0], n)
            query = dict()
            query['portal_type'] = self.portal_type
            query['sample_id'] = new_sampleno
            if not api.content.find(**query):
                break

        return new_sampleno

    def get_unique_barcode(self, barcode):
        pair = barcode.split('-')
        start = 1
        if len(pair) == 2:
            try:
                start = int(pair[(-1)]) + 1
            except ValueError:
                pair[0] = barcode

        new_barcode = ('{0}-{0}').format(pair[0])
        for n in count(start):
            new_barcode = ('{0}-{1}').format(pair[0], n)
            query = dict()
            query['portal_type'] = self.portal_type
            query['sample_id'] = new_barcode
            if not api.content.find(**query):
                break

        return new_barcode


class ChangeStepsEditForm(BaseEditForm):
    """"""
    utils = utils
    fields = field.Fields(IChangeStepsList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = ['sample_id', 'barcode', 'name', 'review_state']
    form_schema = IChangeSteps
    label = _('Change steps')
    _finishedAdd = False

    def dumpOutput(self, data):
        """
        Helper function to see what kind of data DGF submits.
        """
        batch_list = data.get('batch_list', [])
        edit_count = 0
        for entry in batch_list:
            uuid = entry['uuid']
            obj = api.content.uuidToObject(uuid)
            change_note = entry['changeNote']
            if obj:
                old_steps = obj.steps
                if old_steps != entry['steps']:
                    obj.steps = entry['steps']
                    edit_count += 1
                    notify(StepsChangedEvent(obj, old_steps, entry['steps']))
                    change_note = ('{title} {before}->{after}: {note}').format(title=translate(self.label, context=api.portal.getRequest()), before=translate(_(self.steps_group[old_steps]['title']), context=api.portal.getRequest()), after=translate(_(self.steps_group[obj.steps]['title']), context=api.portal.getRequest()), note=change_note if change_note else '')
                    annotation = IAnnotations(self.context.REQUEST)
                    annotation['plone.app.versioningbehavior-changeNote'] = change_note
                    modified(obj)

        if edit_count:
            api.portal.show_message(_('${count} Item edited', mapping={'count': edit_count}), self.request, 'info')
            logger.info(('{count} item edited successfully.').format(count=edit_count))
        return edit_count


class StateTransitionForm(BaseEditForm):
    """"""
    utils = utils
    fields = field.Fields(IStateTransitionList)
    fields['batch_list'].widgetFactory = DataGridFieldFactory
    fields_readonly = ['sample_id', 'barcode', 'name',
     'steps', 'review_state']
    form_schema = IStateTransition
    label = _('State transition')
    _finishedAdd = False

    def datagridInitialise(self, subform, widget):
        """This is called when the subform fields have been initialised,
        but before the widgets have been created.
        Field based configuration could occur here.
        """
        pass

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