# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/export.py
# Compiled at: 2020-01-29 10:23:45
# Size of source mod 2**32: 6705 bytes
from django.core.exceptions import FieldDoesNotExist
from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import force_text
from import_export import fields, resources, widgets
EXPORT_TYPES_TO_CONTENT_TYPES = {'csv':'text/csv', 
 'tsv':'text/tab-separated-values', 
 'xls':'application/vnd.ms-excel', 
 'xlsx':'application/vnd.ms-excel', 
 'ods':'application/vnd.oasis.opendocument.spreadsheet', 
 'json':'application/json', 
 'yaml':'text/plain', 
 'html':'text/html'}

def register_export_action(export_type, label):
    """
    Helper to register export action to specific type. It dynamically
    creates action function and register it as ``admin.site.add_action``
    with passed label.
    """

    def wrapper(modeladmin, request, queryset, *args, **kwargs):
        return export_file(export_type, modeladmin, queryset)

    wrapper.__name__ = 'export_selected_objects_as_{}'.format(export_type)
    wrapper.short_description = label
    admin.site.add_action(wrapper, wrapper.__name__)
    return wrapper


def export_file(export_type, modeladmin, queryset):
    """
    Same as :any:`cms_qe.export.export_data` but wraps it into
    :any:`django.http.HttpResponse` as file to download.
    """
    if export_type not in EXPORT_TYPES_TO_CONTENT_TYPES:
        raise Exception('Type {} is not supported'.format(export_type))
    content_type = EXPORT_TYPES_TO_CONTENT_TYPES[export_type]
    data = export_data(export_type, modeladmin, queryset)
    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="export.{}"'.format(export_type)
    return response


def export_data(export_type, modeladmin, queryset):
    """
    Export data as ``export_type``. Supported are only those in
    constant ``EXPORT_TYPES_TO_CONTENT_TYPES``.
    """
    model_fields = queryset.model._meta.get_fields()

    class ObjectResourceMeta(resources.ModelDeclarativeMetaclass):
        __doc__ = "\n        When model has field with choices, we want to export verbose names\n        instead of keys in database. For that on resource object has to be\n        field with it's list of choices. ``ModelResource`` uses metaclass\n        to collect those data so we need to override that metaclass and\n        pass it manually. Assign it to class after creation is late.\n        "

        def __new__(mcs, name, bases, attrs):
            for field in model_fields:
                choices = getattr(field, 'choices', None)
                if not choices:
                    continue
                attrs[field.name] = fields.Field(attribute=(field.name),
                  widget=(ChoicesWidget(choices)))

            for field_name in modeladmin.list_display:
                if field_name in attrs:
                    continue
                attrs[field_name] = AdminField(attribute=field_name,
                  modeladmin=modeladmin)

            return super().__new__(mcs, name, bases, attrs)

    class ObjectResource(resources.ModelResource, metaclass=ObjectResourceMeta):

        class Meta:
            model = queryset.model
            export_order = [field.name for field in model_fields if field.auto_created if field.name == 'id']

        def get_export_headers(self) -> list:
            """
            As header use verbose name which is better than database name.
            """
            return [self.get_model_field_verbose_name(field) for field in self.get_export_fields()]

        @classmethod
        def get_model_field_verbose_name(cls, field):
            name = cls.get_field_name(field)
            try:
                field = queryset.model._meta.get_field(name)
            except FieldDoesNotExist:
                pass
            else:
                name = force_text(field.verbose_name)
            return name

        def export_field(self, field, obj):
            value = super().export_field(field, obj)
            if '__proxy__' in value.__class__.__name__:
                value = force_text(value)
            return value

    dataset = ObjectResource().export(queryset)
    return getattr(dataset, export_type)


class AdminField(fields.Field):
    __doc__ = '\n    Field to support including extra fields defined in the variable\n    `ModelAdmin.list_display`. Original `fields.Field` is capable\n    to get property so we need to only add support of extra fields\n    defined on the ModelAdmin itself.\n    '

    def __init__(self, *args, **kwds):
        self.modeladmin = kwds.pop('modeladmin')
        (super().__init__)(*args, **kwds)

    def get_value(self, obj):
        admin_property = getattr(self.modeladmin, self.attribute, None)
        if admin_property:
            return admin_property(obj)
        return super().get_value(obj)


class ChoicesWidget(widgets.Widget):
    __doc__ = '\n    Widget that uses choice display values in place of database values\n    '

    def __init__(self, choices, *args, **kwargs):
        """
        Creates a self.choices dict with a key, display value, and value,
        db value, e.g. {'Chocolate': 'CHOC'}
        """
        self.choices = dict(choices)
        self.revert_choices = dict(((v, k) for k, v in self.choices.items()))

    def clean(self, value, row=None, *args, **kwargs):
        """Returns the db value given the display value"""
        if value:
            return self.revert_choices.get(value, value)

    def render(self, value, obj=None):
        """Returns the display value given the db value"""
        return self.choices.get(value, '')