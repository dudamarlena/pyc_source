# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/virtual.py
# Compiled at: 2015-12-07 12:40:35
# Size of source mod 2**32: 6051 bytes
from django.db import models
from django.utils import six
from django.utils.functional import curry
from django import VERSION as DJANGO_VERSION
from .dict import HStoreDict
__all__ = [
 'create_hstore_virtual_field',
 'VirtualField']

class HStoreVirtualMixin(object):
    __doc__ = '\n    must be mixed-in with django fields\n    '
    concrete = False

    def contribute_to_class(self, cls, name):
        if self.choices:
            setattr(cls, 'get_%s_display' % self.name, curry(cls._get_FIELD_display, field=self))
        self.attname = name
        self.name = name
        self.model = cls
        self.column = None
        setattr(cls, name, self)
        if DJANGO_VERSION[:2] >= (1, 8):
            cls._meta.add_field(self, virtual=True)
        else:
            cls._meta.add_field(self)
            cls._meta.virtual_fields.append(self)

    def db_type(self, connection):
        """
        returning None here will cause django to exclude this field
        from the concrete field list (_meta.concrete_fields)
        resulting in the fact that syncdb will skip this field when creating tables in PostgreSQL
        """
        pass

    def deconstruct(self, *args, **kwargs):
        """
        specific for django 1.7 and greater (migration framework)
        """
        name, path, args, kwargs = super(HStoreVirtualMixin, self).deconstruct(*args, **kwargs)
        return (
         name, path, args, {'default': kwargs.get('default'),  'to': None})

    def __get__(self, instance, instance_type=None):
        """
        retrieve value from hstore dictionary
        """
        if instance is None:
            raise AttributeError('Can only be accessed via instance')
        field = getattr(instance, self.hstore_field_name)
        if not field:
            return self.default
        return field.get(self.name, self.default)

    def __set__(self, instance, value):
        """
        set value on hstore dictionary
        """
        hstore_dictionary = getattr(instance, self.hstore_field_name)
        if hstore_dictionary is None:
            setattr(instance, self.hstore_field_name, HStoreDict())
            hstore_dictionary = getattr(instance, self.hstore_field_name)
        hstore_dictionary[self.name] = value


class VirtualField(HStoreVirtualMixin, models.Field):
    __doc__ = '\n    dummy class, used by django 1.7 schema editor only\n    '

    def __init__(self, *args, **kwargs):
        kwargs.pop('to', None)
        super(VirtualField, self).__init__(*args, **kwargs)

        class _Meta(object):

            def __init__(self):
                self.auto_created = False
                self.app_label = 'django_hstore'
                self.model_name = 'virtual'
                self.object_name = self.model_name

        class _Through(object):

            def __init__(self):
                self._meta = _Meta()

        class _Rel(object):

            def __init__(self):
                self.to = self
                self.through = _Through()
                self._meta = _Meta()
                self.parent_link = False

        self.rel = _Rel()
        self.generate_reverse_relation = False


def create_hstore_virtual_field(field_cls, kwargs, hstore_field_name):
    """
    returns an instance of an HStore virtual field which is mixed-in
    with the specified field class and initializated with the kwargs passed
    """
    if isinstance(field_cls, six.string_types):
        try:
            BaseField = getattr(models, field_cls)
        except AttributeError:
            raise ValueError("specified class %s is not a standard django model field (couldn't find it in django.db.models)" % field_cls)

    else:
        if issubclass(field_cls, models.Field):
            BaseField = field_cls
        else:
            raise ValueError('field must be either a django standard field or a subclass of django.db.models.Field')

        class VirtualField(HStoreVirtualMixin):
            __basefield__ = BaseField

        VirtualField.hstore_field_name = hstore_field_name
        if BaseField == models.DateTimeField:
            if kwargs.get('null') or kwargs.get('blank'):
                kwargs['default'] = None
        if BaseField == models.DateTimeField or BaseField == models.DateField:

            def value_to_string(self, obj):
                val = self._get_val_from_obj(obj)
                try:
                    if val is None:
                        return ''
                    else:
                        return val.isoformat()
                except AttributeError:
                    return val

            VirtualField.value_to_string = value_to_string
        field = VirtualField(**kwargs)
        if field.default == models.fields.NOT_PROVIDED:
            field.default = ''
        return field


try:
    from south.modelsinspector import add_ignored_fields
    add_ignored_fields(['^django_hstore\\.virtual\\.VirtualField'])
except ImportError:
    pass