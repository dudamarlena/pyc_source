# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/meta/views.py
# Compiled at: 2015-02-24 06:29:06
# Size of source mod 2**32: 7909 bytes
import contextlib, inspect
from os import path
from django.contrib.auth.models import User
from django.utils.module_loading import import_string
from django.utils import six
from ginger import forms
from ginger import views as generics
from ginger import patch, utils
from django.apps import apps
from . import templates
from .app import Application

class ViewPatch(object):

    def __init__(self, view_class):
        if isinstance(view_class, six.string_types):
            view_class = import_string(view_class)
        self.view_class = view_class
        self.meta = view_class.meta
        self.app = Application(self.meta.app.label)
        self.module = inspect.getmodule(self.view_class)
        self.model = self.get_model()

    def get_kind(self):
        if issubclass(self.view_class, generics.GingerNewView):
            return 'new'
        if issubclass(self.view_class, generics.GingerEditView):
            return 'edit'
        if issubclass(self.view_class, generics.GingerDeleteView):
            return 'delete'
        if issubclass(self.view_class, generics.GingerSearchView):
            return 'search'
        if issubclass(self.view_class, generics.GingerListView):
            return 'list'
        if issubclass(self.view_class, generics.GingerFormView):
            return 'form'
        if issubclass(self.view_class, generics.GingerTemplateView):
            return 'template'
        return 'template'

    @contextlib.contextmanager
    def class_patch(self):
        module = patch.Module(self.module)
        class_ = module.Class(self.view_class)
        yield class_
        module.save()

    def get_model(self):
        view = self.view_class
        model = getattr(view, 'model', None)
        if model:
            return model
        parts = self.meta.resource_name.split('_')
        app_label = self.app.label
        while parts:
            class_name = ''.join(p.capitalize() for p in parts)
            try:
                model = apps.get_model(app_label, class_name)
            except LookupError:
                model = next((m for m in apps.get_models() if m.__name__ == class_name), None)

            if model:
                return model
            parts.pop(0)

    def patch(self):
        kind = self.get_kind()
        method = 'patch_%s_view' % kind
        return getattr(self, method)()

    def create_template(self, content, context=None, filename=None):
        if context is None:
            context = {}
        defaults = {'app_name': self.app.label, 
         'resource_name': self.meta.resource_name}
        defaults.update(context)
        if filename is None:
            filename = self.meta.template_path
        templates.Template(filename, content).render(defaults)

    def patch_form_view(self):
        model = self.model
        base = forms.GingerForm if not model else forms.GingerModelForm
        module = patch.Module(self.app.form_module)
        cls = module.Class(self.meta.form_name, [base])
        form_class = cls
        if model:
            meta_cls = form_class.Class('Meta')
            meta_cls.Attr('model', model)
            meta_cls.Attr('exclude', ())
            func = form_class.Def('execute', ['user'])
        module.save()
        with self.class_patch() as (cls):
            cls.Attr('form_class', form_class)
            if model:
                cls.Attr('model', model)
        self.create_template(templates.FORM_TEMPLATE)

    def patch_delete_view(self):
        model = self.model
        base = forms.GingerForm if not model else forms.GingerModelForm
        module = patch.Module(self.app.form_module)
        cls = module.Class(self.meta.form_name, [base])
        form_class = cls
        if model:
            meta_cls = form_class.Class('Meta')
            meta_cls.Attr('model', model)
            meta_cls.Attr('fields', ())
            func = form_class.Def('execute', ['user', 'instance'])
            func('\n            instance.delete()\n            ')
        module.save()
        with self.class_patch() as (cls):
            cls.Attr('form_class', form_class)
            if model:
                cls.Attr('model', model)
        self.create_template(templates.FORM_TEMPLATE)

    def patch_new_view(self):
        model = self.model
        base = forms.GingerForm if not model else forms.GingerModelForm
        module = patch.Module(self.app.form_module)
        cls = module.Class(self.meta.form_name, [base])
        form_class = cls
        if model:
            meta_cls = form_class.Class('Meta')
            meta_cls.Attr('model', model)
            meta_cls.Attr('exclude', ())
            func = form_class.Def('execute', ['user', 'instance'])
            func('\n            instance.save()\n            ')
        module.save()
        with self.class_patch() as (cls):
            cls.Attr('form_class', form_class)
            if model:
                cls.Attr('model', model)
        self.create_template(templates.FORM_TEMPLATE)

    def patch_edit_view(self):
        model = self.model
        base = forms.GingerForm if not model else forms.GingerModelForm
        module = patch.Module(self.app.form_module)
        cls = module.Class(self.meta.form_name, [base])
        form_class = cls
        if model:
            meta_cls = form_class.Class('Meta')
            meta_cls.Attr('model', model)
            meta_cls.Attr('exclude', ())
            func = form_class.Def('execute', ['user', 'instance'])
            func('\n            instance.save()\n            return instance\n            ')
        module.save()
        with self.class_patch() as (cls):
            cls.Attr('form_class', form_class)
            if model:
                cls.Attr('model', model)
        self.create_template(templates.FORM_TEMPLATE)

    def patch_list_view(self):
        self.create_template(templates.LIST_TEMPLATE)
        self.create_template(templates.LIST_ITEM_TEMPLATE, filename=path.join(self.meta.template_dir, '%s/include/%s_item.html' % (self.app.label,
         self.meta.resource_name)))

    def patch_search_view(self):
        model = self.model
        base = forms.GingerSearchForm if not model else forms.GingerSearchModelForm
        module = patch.Module(self.app.form_module)
        cls = module.Class(self.meta.form_name, [base])
        form_class = cls
        if model:
            meta_cls = form_class.Class('Meta')
            meta_cls.Attr('model', model)
            meta_cls.Attr('exclude', ())
            func = form_class.Def('get_queryset', [], varkw='kwargs')
            func('\n            return {model}.objects.all()\n            ', model=model)
        module.save()
        with self.class_patch() as (cls):
            cls.Attr('form_class', form_class)
            if model:
                cls.Attr('model', model)
        self.create_template(templates.LIST_TEMPLATE)
        self.create_template(templates.LIST_ITEM_TEMPLATE, filename=path.join(self.meta.template_dir, '%s/include/%s_item.html' % (self.app.label,
         self.meta.resource_name)))

    def patch_template_view(self):
        self.create_template(templates.SIMPLE_TEMPLATE)

    def __str__(self):
        return str(dict(app_label=self.app.label, template_dir=self.meta.template_dir, template_name=self.meta.template_name, template_path=self.meta.template_path, resource_name=self.meta.resource_name, form_name=self.meta.form_name, form_path=self.meta.form_path, verb=self.meta.verb))