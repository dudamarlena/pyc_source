# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/modelsinspector.py
# Compiled at: 2018-07-11 18:15:31
"""
Like the old south.modelsparser, but using introspection where possible
rather than direct inspection of models.py.
"""
from __future__ import print_function
import datetime, re, decimal
from south.utils import get_attribute, auto_through
from south.utils.py3 import text_type
from django.db import models
from django.db.models.base import ModelBase, Model
from django.db.models.fields import NOT_PROVIDED
from django.conf import settings
from django.utils.functional import Promise
from django.contrib.contenttypes import generic
from django.utils.datastructures import SortedDict
from django.utils import datetime_safe
NOISY = False
try:
    from django.utils import timezone
except ImportError:
    timezone = False

def convert_on_delete_handler(value):
    django_db_models_module = 'models'
    if hasattr(models, 'PROTECT'):
        if value in (models.CASCADE, models.PROTECT, models.DO_NOTHING, models.SET_DEFAULT):
            return '%s.%s' % (django_db_models_module, value.__name__)
        func_name = getattr(value, '__name__', None)
        if func_name == 'set_on_delete':
            closure_contents = value.__closure__[0].cell_contents
            if closure_contents is None:
                return '%s.SET_NULL' % django_db_models_module
            if hasattr(closure_contents, '__call__'):
                raise ValueError('South does not support on_delete with SET(function) as values.')
            else:
                return '%s.SET(%s)' % (django_db_models_module, value_clean(closure_contents))
        raise ValueError('%s was not recognized as a valid model deletion handler. Possible values: %s.' % (value, (', ').join(f.__name__ for f in (models.CASCADE, models.PROTECT, models.SET, models.SET_NULL, models.SET_DEFAULT, models.DO_NOTHING))))
    else:
        raise ValueError('on_delete argument encountered in Django version that does not support it')
    return


introspection_details = [
 (
  (
   models.Field,), [],
  {'null': [
            'null', {'default': False}], 
     'blank': [
             'blank', {'default': False, 'ignore_if': 'primary_key'}], 
     'primary_key': [
                   'primary_key', {'default': False}], 
     'max_length': [
                  'max_length', {'default': None}], 
     'unique': [
              '_unique', {'default': False}], 
     'db_index': [
                'db_index', {'default': False}], 
     'default': [
               'default', {'default': NOT_PROVIDED, 'ignore_dynamics': True}], 
     'db_column': [
                 'db_column', {'default': None}], 
     'db_tablespace': [
                     'db_tablespace', {'default': settings.DEFAULT_INDEX_TABLESPACE}]}),
 (
  (
   models.ForeignKey, models.OneToOneField), [],
  dict([
   (
    'to', ['rel.to', {}]),
   (
    'to_field', ['rel.field_name', {'default_attr': 'rel.to._meta.pk.name'}]),
   (
    'related_name', ['rel.related_name', {'default': None}]),
   (
    'db_index', ['db_index', {'default': True}]),
   (
    'on_delete', ['rel.on_delete', {'default': getattr(models, 'CASCADE', None), 'is_django_function': True, 'converter': convert_on_delete_handler, 'ignore_missing': True}])])),
 (
  (
   models.ManyToManyField,), [],
  {'to': [
          'rel.to', {}], 
     'symmetrical': [
                   'rel.symmetrical', {'default': True}], 
     'related_name': [
                    'rel.related_name', {'default': None}], 
     'db_table': [
                'db_table', {'default': None}], 
     'through': [
               'rel.through', {'ignore_if_auto_through': True}]}),
 (
  (
   models.DateField, models.TimeField), [],
  {'auto_now': [
                'auto_now', {'default': False}], 
     'auto_now_add': [
                    'auto_now_add', {'default': False}]}),
 (
  (
   models.DecimalField,), [],
  {'max_digits': [
                  'max_digits', {'default': None}], 
     'decimal_places': [
                      'decimal_places', {'default': None}]}),
 (
  (
   models.SlugField,), [],
  {'db_index': [
                'db_index', {'default': True}]}),
 (
  (
   models.BooleanField,), [],
  {'default': [
               'default', {'default': NOT_PROVIDED, 'converter': bool}], 
     'blank': [
             'blank', {'default': True, 'ignore_if': 'primary_key'}]}),
 (
  (
   models.FilePathField,), [],
  {'path': [
            'path', {'default': ''}], 
     'match': [
             'match', {'default': None}], 
     'recursive': [
                 'recursive', {'default': False}]}),
 (
  (
   generic.GenericRelation,), [],
  {'to': [
          'rel.to', {}], 
     'symmetrical': [
                   'rel.symmetrical', {'default': True}], 
     'object_id_field': [
                       'object_id_field_name', {'default': 'object_id'}], 
     'content_type_field': [
                          'content_type_field_name', {'default': 'content_type'}], 
     'blank': [
             'blank', {'default': True}]})]
allowed_fields = [
 '^django\\.db',
 '^django\\.contrib\\.contenttypes\\.generic',
 '^django\\.contrib\\.localflavor',
 '^django_localflavor_\\w\\w']
ignored_fields = [
 '^django\\.contrib\\.contenttypes\\.generic\\.GenericRelation',
 '^django\\.contrib\\.contenttypes\\.generic\\.GenericForeignKey']
meta_details = {'db_table': [
              'db_table', {'default_attr_concat': ['%s_%s', 'app_label', 'module_name']}], 
   'db_tablespace': [
                   'db_tablespace', {'default': settings.DEFAULT_TABLESPACE}], 
   'unique_together': [
                     'unique_together', {'default': []}], 
   'index_together': [
                    'index_together', {'default': [], 'ignore_missing': True}], 
   'ordering': [
              'ordering', {'default': []}], 
   'proxy': [
           'proxy', {'default': False, 'ignore_missing': True}]}

def add_introspection_rules(rules=[], patterns=[]):
    """Allows you to add some introspection rules at runtime, e.g. for 3rd party apps."""
    assert isinstance(rules, (list, tuple))
    assert isinstance(patterns, (list, tuple))
    allowed_fields.extend(patterns)
    introspection_details.extend(rules)


def add_ignored_fields(patterns):
    """Allows you to add some ignore field patterns."""
    assert isinstance(patterns, (list, tuple))
    ignored_fields.extend(patterns)


def can_ignore(field):
    """
    Returns True if we know for certain that we can ignore this field, False
    otherwise.
    """
    full_name = '%s.%s' % (field.__class__.__module__, field.__class__.__name__)
    for regex in ignored_fields:
        if re.match(regex, full_name):
            return True

    return False


def can_introspect(field):
    """
    Returns True if we are allowed to introspect this field, False otherwise.
    ('allowed' means 'in core'. Custom fields can declare they are introspectable
    by the default South rules by adding the attribute _south_introspects = True.)
    """
    if hasattr(field, '_south_introspects') and field._south_introspects:
        return True
    full_name = '%s.%s' % (field.__class__.__module__, field.__class__.__name__)
    for regex in allowed_fields:
        if re.match(regex, full_name):
            return True

    return False


def matching_details(field):
    """
    Returns the union of all matching entries in introspection_details for the field.
    """
    our_args = []
    our_kwargs = {}
    for classes, args, kwargs in introspection_details:
        if any([ isinstance(field, x) for x in classes ]):
            our_args.extend(args)
            our_kwargs.update(kwargs)

    return (
     our_args, our_kwargs)


class IsDefault(Exception):
    """
    Exception for when a field contains its default value.
    """
    pass


def get_value(field, descriptor):
    """
    Gets an attribute value from a Field instance and formats it.
    """
    attrname, options = descriptor
    if options.get('is_value', False):
        value = attrname
    else:
        try:
            value = get_attribute(field, attrname)
        except AttributeError:
            if options.get('ignore_missing', False):
                raise IsDefault
            else:
                raise

    if isinstance(value, Promise):
        value = text_type(value)
    if 'default' in options and value == options['default']:
        raise IsDefault
    if 'ignore_if' in options:
        if get_attribute(field, options['ignore_if']):
            raise IsDefault
    if options.get('ignore_if_auto_through', False):
        if auto_through(field):
            raise IsDefault
    if 'default_attr' in options:
        default_value = get_attribute(field, options['default_attr'])
        if value == default_value:
            raise IsDefault
    if 'default_attr_concat' in options:
        format, attrs = options['default_attr_concat'][0], options['default_attr_concat'][1:]
        default_value = format % tuple(map(lambda x: get_attribute(field, x), attrs))
        if value == default_value:
            raise IsDefault
    return value_clean(value, options)


def value_clean(value, options={}):
    """Takes a value and cleans it up (so e.g. it has timezone working right)"""
    if isinstance(value, Promise):
        value = text_type(value)
    if not options.get('is_django_function', False) and callable(value) and not isinstance(value, ModelBase):
        if value == datetime.datetime.now:
            return 'datetime.datetime.now'
        if value == datetime.datetime.utcnow:
            return 'datetime.datetime.utcnow'
        if value == datetime.date.today:
            return 'datetime.date.today'
        if timezone and value == timezone.now:
            return 'datetime.datetime.now'
        value = value()
    if isinstance(value, ModelBase):
        if getattr(value._meta, 'proxy', False):
            value = value._meta.proxy_for_model
        return "orm['%s.%s']" % (value._meta.app_label, value._meta.object_name)
    else:
        if isinstance(value, Model):
            if options.get('ignore_dynamics', False):
                raise IsDefault
            return "orm['%s.%s'].objects.get(pk=%r)" % (value.__class__._meta.app_label, value.__class__._meta.object_name, value.pk)
        else:
            if isinstance(value, decimal.Decimal):
                value = str(value)
            datetime_types = (
             datetime.datetime,
             datetime.time,
             datetime_safe.datetime)
            if timezone and isinstance(value, datetime_types) and getattr(settings, 'USE_TZ', False) and value is not None and timezone.is_aware(value):
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_naive(value, default_timezone)
            if isinstance(value, datetime_safe.datetime):
                value = datetime.datetime(*value.utctimetuple()[:7])
            else:
                if isinstance(value, (datetime.date, datetime_safe.date)):
                    value = datetime.datetime(*value.timetuple()[:3])
                if 'converter' in options:
                    value = options['converter'](value)
                if options.get('is_django_function', False):
                    return value
            return repr(value)

        return


def introspector(field):
    """
    Given a field, introspects its definition triple.
    """
    arg_defs, kwarg_defs = matching_details(field)
    args = []
    kwargs = {}
    for defn in arg_defs:
        try:
            args.append(get_value(field, defn))
        except IsDefault:
            pass

    for kwd, defn in kwarg_defs.items():
        try:
            kwargs[kwd] = get_value(field, defn)
        except IsDefault:
            pass

    return (
     args, kwargs)


def get_model_fields(model, m2m=False):
    """
    Given a model class, returns a dict of {field_name: field_triple} defs.
    """
    field_defs = SortedDict()
    inherited_fields = {}
    for base in model.__bases__:
        if hasattr(base, '_meta') and issubclass(base, models.Model):
            if not base._meta.abstract:
                inherited_fields.update(get_model_fields(base))

    source = model._meta.local_fields[:]
    if m2m:
        source += model._meta.local_many_to_many
    for field in source:
        if can_ignore(field):
            continue
        if hasattr(field, 'south_field_triple'):
            if NOISY:
                print(' ( Nativing field: %s' % field.name)
            field_defs[field.name] = field.south_field_triple()
        elif can_introspect(field):
            field_class = field.__class__.__module__ + '.' + field.__class__.__name__
            args, kwargs = introspector(field)
            if model._meta.pk.column == field.column and 'primary_key' not in kwargs:
                kwargs['primary_key'] = True
            field_defs[field.name] = (field_class, args, kwargs)
        else:
            if NOISY:
                print(' ( Nodefing field: %s' % field.name)
            field_defs[field.name] = None

    if model._meta.order_with_respect_to:
        field_defs['_order'] = (
         'django.db.models.fields.IntegerField', [], {'default': '0'})
    return field_defs


def get_model_meta(model):
    """
    Given a model class, will return the dict representing the Meta class.
    """
    meta_def = {}
    for kwd, defn in meta_details.items():
        try:
            meta_def[kwd] = get_value(model._meta, defn)
        except IsDefault:
            pass

    for base in model.__bases__:
        if hasattr(base, '_meta') and issubclass(base, models.Model):
            if not base._meta.abstract:
                if '_ormbases' not in meta_def:
                    meta_def['_ormbases'] = []
                meta_def['_ormbases'].append('%s.%s' % (
                 base._meta.app_label,
                 base._meta.object_name))

    return meta_def


import south.introspection_plugins