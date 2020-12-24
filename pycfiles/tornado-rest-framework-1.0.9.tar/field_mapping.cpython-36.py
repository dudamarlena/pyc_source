# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/field_mapping.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 10947 bytes
"""
Helper functions for mapping model fields to a dictionary of default
keyword arguments that should be used for their equivalent serializer fields.
"""
import inspect
from django.core import validators
from django.db import models
from django.utils.text import capfirst
from rest_framework.compat import postgres_fields
from rest_framework.validators import UniqueValidator
NUMERIC_FIELD_TYPES = (
 models.IntegerField, models.FloatField, models.DecimalField)

class ClassLookupDict(object):
    __doc__ = "\n    Takes a dictionary with classes as keys.\n    Lookups against this object will traverses the object's inheritance\n    hierarchy in method resolution order, and returns the first matching value\n    from the dictionary or raises a KeyError if nothing matches.\n    "

    def __init__(self, mapping):
        self.mapping = mapping

    def __getitem__(self, key):
        if hasattr(key, '_proxy_class'):
            base_class = key._proxy_class
        else:
            base_class = key.__class__
        for cls in inspect.getmro(base_class):
            if cls in self.mapping:
                return self.mapping[cls]

        raise KeyError('Class %s not found in lookup.' % base_class.__name__)

    def __setitem__(self, key, value):
        self.mapping[key] = value


def needs_label(model_field, field_name):
    """
    Returns `True` if the label based on the model's verbose name
    is not equal to the default label it would have based on it's field name.
    """
    default_label = field_name.replace('_', ' ').capitalize()
    return capfirst(model_field.verbose_name) != default_label


def get_detail_view_name(model):
    """
    Given a model class, return the view name to use for URL relationships
    that refer to instances of the model.
    """
    return '%(model_name)s-detail' % {'app_label':model._meta.app_label, 
     'model_name':model._meta.object_name.lower()}


def get_field_kwargs(field_name, model_field):
    """
    Creates a default instance of a basic non-relational field.
    """
    kwargs = {}
    validator_kwarg = list(model_field.validators)
    kwargs['model_field'] = model_field
    if model_field.verbose_name:
        if needs_label(model_field, field_name):
            kwargs['label'] = capfirst(model_field.verbose_name)
    if model_field.help_text:
        kwargs['help_text'] = model_field.help_text
    max_digits = getattr(model_field, 'max_digits', None)
    if max_digits is not None:
        kwargs['max_digits'] = max_digits
    decimal_places = getattr(model_field, 'decimal_places', None)
    if decimal_places is not None:
        kwargs['decimal_places'] = decimal_places
    if isinstance(model_field, models.TextField) or postgres_fields and isinstance(model_field, postgres_fields.JSONField):
        kwargs['style'] = {'base_template': 'textarea.html'}
    if isinstance(model_field, models.AutoField) or not model_field.editable:
        kwargs['read_only'] = True
        return kwargs
    else:
        if model_field.has_default() or model_field.blank or model_field.null:
            kwargs['required'] = False
        else:
            if model_field.null:
                if not isinstance(model_field, models.NullBooleanField):
                    kwargs['allow_null'] = True
                else:
                    if model_field.blank:
                        if isinstance(model_field, models.CharField) or isinstance(model_field, models.TextField):
                            kwargs['allow_blank'] = True
                        if isinstance(model_field, models.FilePathField):
                            kwargs['path'] = model_field.path
                            if model_field.match is not None:
                                kwargs['match'] = model_field.match
                            if model_field.recursive is not False:
                                kwargs['recursive'] = model_field.recursive
                            if model_field.allow_files is not True:
                                kwargs['allow_files'] = model_field.allow_files
                            if model_field.allow_folders is not False:
                                kwargs['allow_folders'] = model_field.allow_folders
                        if model_field.choices:
                            kwargs['choices'] = model_field.choices
                        else:
                            max_value = next((validator.limit_value for validator in validator_kwarg if isinstance(validator, validators.MaxValueValidator)), None)
                            if max_value is not None:
                                if isinstance(model_field, NUMERIC_FIELD_TYPES):
                                    kwargs['max_value'] = max_value
                                    validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.MaxValueValidator)]
                            min_value = next((validator.limit_value for validator in validator_kwarg if isinstance(validator, validators.MinValueValidator)), None)
                            if min_value is not None:
                                if isinstance(model_field, NUMERIC_FIELD_TYPES):
                                    kwargs['min_value'] = min_value
                                    validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.MinValueValidator)]
                            if isinstance(model_field, models.URLField):
                                validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.URLValidator)]
                            if isinstance(model_field, models.EmailField):
                                validator_kwarg = [validator for validator in validator_kwarg if validator is not validators.validate_email]
                            if isinstance(model_field, models.SlugField):
                                validator_kwarg = [validator for validator in validator_kwarg if validator is not validators.validate_slug]
                            if isinstance(model_field, models.GenericIPAddressField):
                                validator_kwarg = [validator for validator in validator_kwarg if validator is not validators.validate_ipv46_address]
                    elif isinstance(model_field, models.DecimalField):
                        validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.DecimalValidator)]
                    max_length = getattr(model_field, 'max_length', None)
                    if max_length is not None:
                        if isinstance(model_field, models.CharField) or isinstance(model_field, models.TextField) or isinstance(model_field, models.FileField):
                            kwargs['max_length'] = max_length
                            validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.MaxLengthValidator)]
            else:
                min_length = next((validator.limit_value for validator in validator_kwarg if isinstance(validator, validators.MinLengthValidator)), None)
                if min_length is not None:
                    if isinstance(model_field, models.CharField):
                        kwargs['min_length'] = min_length
                        validator_kwarg = [validator for validator in validator_kwarg if not isinstance(validator, validators.MinLengthValidator)]
                if getattr(model_field, 'unique', False):
                    unique_error_message = model_field.error_messages.get('unique', None)
                    if unique_error_message:
                        unique_error_message = unique_error_message % {'model_name':model_field.model._meta.verbose_name, 
                         'field_label':model_field.verbose_name}
                    validator = UniqueValidator(queryset=(model_field.model._default_manager),
                      message=unique_error_message)
                    validator_kwarg.append(validator)
            if validator_kwarg:
                kwargs['validators'] = validator_kwarg
        return kwargs


def get_relation_kwargs(field_name, relation_info):
    """
    Creates a default instance of a flat relational field.
    """
    model_field, related_model, to_many, to_field, has_through_model, reverse = relation_info
    kwargs = {'queryset':related_model._default_manager, 
     'view_name':get_detail_view_name(related_model)}
    if to_many:
        kwargs['many'] = True
    if to_field:
        kwargs['to_field'] = to_field
    if has_through_model:
        kwargs['read_only'] = True
        kwargs.pop('queryset', None)
    if model_field:
        if model_field.verbose_name:
            if needs_label(model_field, field_name):
                kwargs['label'] = capfirst(model_field.verbose_name)
            else:
                help_text = model_field.help_text
                if help_text:
                    kwargs['help_text'] = help_text
                if not model_field.editable:
                    kwargs['read_only'] = True
                    kwargs.pop('queryset', None)
                if kwargs.get('read_only', False):
                    return kwargs
                if model_field.has_default() or model_field.blank or model_field.null:
                    kwargs['required'] = False
                if model_field.null:
                    kwargs['allow_null'] = True
                if model_field.validators:
                    kwargs['validators'] = model_field.validators
            if getattr(model_field, 'unique', False):
                validator = UniqueValidator(queryset=(model_field.model._default_manager))
                kwargs['validators'] = kwargs.get('validators', []) + [validator]
        else:
            if to_many:
                if not model_field.blank:
                    kwargs['allow_empty'] = False
    return kwargs


def get_nested_relation_kwargs(relation_info):
    kwargs = {'read_only': True}
    if relation_info.to_many:
        kwargs['many'] = True
    return kwargs


def get_url_kwargs(model_field):
    return {'view_name': get_detail_view_name(model_field)}