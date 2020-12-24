# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/forms.py
# Compiled at: 2017-06-09 03:04:34
import sys, colander, deform
from types import ClassType
from pyramid.decorator import reify
from pyramid_deform import CSRFSchema
from pyramid_deform import FormView
from pyramid.httpexceptions import HTTPFound
from kotti_controlpanel.events import SettingsAfterSave
from kotti_controlpanel.events import SettingsBeforeSave
from kotti_controlpanel.util import get_settings, get_setting, set_setting
from kotti_controlpanel import _
import itertools
counter = itertools.count()

class SettingsSchema(colander.MappingSchema):
    """An empty schema to have a named one if needed.
    """
    pass


class SettingsFormView(FormView):
    """The form template class for one setting tab.
    """
    name = 'settings'
    title = _('Settings')
    description = ''
    success_message = _('Your changes have been saved. Please reload the application for it to take effect.')
    success_url = None
    settings = None
    schema_factory = None
    use_csrf_token = True
    use_ajax = False
    active = False
    form_options = {'counter': counter}

    def __init__(self, context, request, **kwargs):
        self.context = context
        self.request = request
        self.__dict__.update(kwargs)

    def form_class(self, *args, **kwargs):
        form = deform.form.Form(*args, **kwargs)
        form.formid = self.form_id
        return form

    def __call__(self):
        """Build up the schema and return the form view.
        """
        if self.schema is None:
            if self.schema_factory is None:
                self.schema_factory = SettingsSchema
            self.schema = self.schema_factory()
        if self.use_csrf_token and 'csrf_token' not in self.schema:
            self.schema.children.append(CSRFSchema()['csrf_token'])
        for setting_obj in self.settings.settings_objs:
            node = colander.SchemaNode(self.colander_type(setting_obj.type)(), name=setting_obj.field_name, title=setting_obj.title, description=setting_obj.description, default=setting_obj.default)
            self.schema.children.append(node)

        settings = get_settings()
        bind_values = self.settings.bind.copy()
        for child in self.schema.children:
            bind_attrs = bind_values.get(child.name, None)
            if child.name == 'csrf_token':
                continue
            if not child.name.startswith(self.settings.module):
                child.name = '%s-%s' % (self.settings.module, child.name)
                child.default = settings.get(child.name)
            if bind_attrs:
                for k, v in bind_attrs.iteritems():
                    if callable(v):
                        v = v()
                    setattr(child, k, v)

        save = 'save_' + self.form_id
        self.buttons = (
         deform.Button(save, _('Save')),
         deform.Button('cancel', _('Cancel')))
        setattr(self, save + '_success', self.save_success)
        return super(SettingsFormView, self).__call__()

    @reify
    def form_id(self):
        form_id = ('{0}-{1}').format(self.settings.module, self.name)
        return form_id

    def colander_type(self, name):
        try:
            klass = getattr(sys.modules['colander'], name)
        except AttributeError:
            raise NameError('%s is not an sqlalchemy data type.' % name)

        if isinstance(klass, (ClassType, type)):
            return klass
        raise TypeError('%s is not a class.' % name)

    def save_success(self, appstruct):
        formid = self.request.POST.get('__formid__', None)
        self.active = False
        if formid is not None and formid == self.form_id:
            self.active = True
            appstruct.pop('csrf_token', None)
            module = None
            if appstruct:
                key = appstruct.keys()[0]
                module = key[:key.find('-')]
            self.request.registry.notify(SettingsBeforeSave(module))
            for item in appstruct:
                if appstruct[item] is not None:
                    set_setting(item, appstruct[item])

            ses = self.request.session
            if '_f_success' not in ses or self.success_message not in ses['_f_success']:
                self.request.session.flash(self.success_message, 'success')
            self.request.registry.notify(SettingsAfterSave(module))
        return

    def cancel_success(self, appstruct):
        self.request.session.flash(_('No changes made.'), 'info')
        location = self.request.resource_url(self.context, 'controlpanel')
        raise HTTPFound(location=location)