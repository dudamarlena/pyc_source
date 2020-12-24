# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/leo/Devel/Naeka/wagtailmodelchooser/wagtailmodelchooser/edit_handlers.py
# Compiled at: 2018-10-30 12:34:47
# Size of source mod 2**32: 5187 bytes
from django.conf import settings
from django.conf.urls import url
from django.db import models
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from wagtail.admin.edit_handlers import BaseChooserPanel
from wagtail.core import hooks
from .widgets import AdminModelChooser
from .views import ModelChooserView, ModelChosenView

class ModelChooserPanel(BaseChooserPanel):
    object_type_name = 'model'
    widget_class = None
    model = None
    chooser_view = None
    chosen_view = None

    def widget_overrides(self):
        return {self.field_name: self.widget_class}

    @classmethod
    def register_with_wagtail(cls):

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return cls.get_admin_urls_for_registration()

        @hooks.register('insert_editor_js')
        def insert_editor_js():
            return cls.get_editor_js_for_registration()

    @classmethod
    def get_admin_urls_for_registration(cls):
        return (
         url(('^{}/chooser/$'.format(cls.model._meta.model_name)), (cls.chooser_view.as_view()), name=('{}_chooser'.format(cls.model._meta.model_name))),
         url(('^{}/chooser/(?P<pk>\\d+)/$'.format(cls.model._meta.model_name)), (cls.chosen_view.as_view()), name=('{}_chosen'.format(cls.model._meta.model_name))))

    @classmethod
    def get_editor_js_for_registration(cls):
        js_files = cls.get_editor_js_files()
        js_includes = format_html_join('\n', '<script src="{0}{1}"></script>', ((settings.STATIC_URL, filename) for filename in js_files))
        return js_includes + format_html("\n            <script>\n                window.chooserUrls.{0}Chooser = '{1}';\n            </script>\n            ", cls.model._meta.object_name, reverse('{}_chooser'.format(cls.model._meta.model_name)))

    @classmethod
    def get_editor_js_files(cls):
        return [
         'wagtailmodelchooser/js/model-chooser.js']


def register_chooser_for_model(model, widget_class=None, widget_attrs={}, chooser_panel_base_class=None, chooser_view=None, chooser_view_attrs={}, chosen_view=None, chosen_view_attrs={}, title_field='title'):
    if not issubclass(model, models.Model):
        raise AssertionError("model must be a subclass of Django's models.Model")
    else:
        class_name = model._meta.object_name
        if widget_class and not getattr(widget_class, 'model', None) == model:
            raise AssertionError("Incorrect model attribute for {}: '{}.{}' is expected".format(widget_class.__name__, model.__module__, model.__name__))
        else:
            defaults = {'model':model, 
             'title_field':title_field}
            (defaults.update)(**widget_attrs)
            widget_class = type(str('Admin{}Chooser'.format(class_name)), (AdminModelChooser,), defaults)
        if chooser_view:
            assert getattr(chooser_view, 'model', None) == model, "Incorrect model attribute for {}: '{}.{}' is expected".format(chooser_view.__name__, model.__module__, model.__name__)
            assert hasattr(chooser_view, 'title_field'), "chooser_view must define 'title_field'"
            assert hasattr(chooser_view, 'model_chooser_url_name'), "chooser_view must define 'model_chooser_url_name'"
            if not hasattr(chooser_view, 'model_chosen_url_name'):
                raise AssertionError("chooser_view must define 'model_chosen_url_name'")
            else:
                defaults = {'model':model, 
                 'ordering':[
                  '-pk'], 
                 'title_field':title_field, 
                 'model_chooser_url_name':'{}_chooser'.format(model._meta.model_name), 
                 'model_chosen_url_name':'{}_chosen'.format(model._meta.model_name)}
                (defaults.update)(**chooser_view_attrs)
                chooser_view = type(str('{}ChooserView'.format(class_name)), (ModelChooserView,), defaults)
        elif chosen_view:
            assert getattr(chosen_view, 'model', None) == model, "Incorrect model attribute for {}: '{}.{}' is expected".format(chosen_view.__name__, model.__module__, model.__name__)
            assert hasattr(chosen_view, 'title_field'), "chooser_view must define 'title_field'"
        else:
            defaults = {'model':model, 
             'title_field':title_field}
            (defaults.update)(**chosen_view_attrs)
            chosen_view = type(str('{}ChosenView'.format(class_name)), (ModelChosenView,), defaults)
    chooser_panel_class = type(str('{}ChooserPanel'.format(class_name)), (ModelChooserPanel,), {'object_type_name':model._meta.model_name, 
     'widget_class':widget_class, 
     'model':model, 
     'chooser_view':chooser_view, 
     'chosen_view':chosen_view})
    chooser_panel_class.register_with_wagtail()
    return chooser_panel_class