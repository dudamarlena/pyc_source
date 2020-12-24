# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/fields/json.py
# Compiled at: 2018-07-31 07:31:31
# Size of source mod 2**32: 11365 bytes
try:
    from django.contrib.postgres.fields import JSONField
except ImportError:
    import copy
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    try:
        from django.utils import six
    except ImportError:
        import six

    try:
        import json
    except ImportError:
        from django.utils import simplejson as json

    from django.forms import fields
    try:
        from django.forms.utils import ValidationError
    except ImportError:
        from django.forms.util import ValidationError

    class SubfieldBase(type):
        __doc__ = "\n        A metaclass for custom Field subclasses. This ensures the model's attribute\n        has the descriptor protocol attached to it.\n        "

        def __new__(cls, name, bases, attrs):
            new_class = super(SubfieldBase, cls).__new__(cls, name, bases, attrs)
            new_class.contribute_to_class = make_contrib(new_class, attrs.get('contribute_to_class'))
            return new_class


    class Creator(object):
        __doc__ = '\n        A placeholder class that provides a way to set the attribute on the model.\n        '

        def __init__(self, field):
            self.field = field

        def __get__(self, obj, type=None):
            if obj is None:
                return self
            else:
                return obj.__dict__[self.field.name]

        def __set__(self, obj, value):
            obj.__dict__[self.field.name] = self.field.pre_init(value, obj)


    def make_contrib(superclass, func=None):
        """
        Returns a suitable contribute_to_class() method for the Field subclass.

        If 'func' is passed in, it is the existing contribute_to_class() method on
        the subclass and it is called before anything else. It is assumed in this
        case that the existing contribute_to_class() calls all the necessary
        superclass methods.
        """

        def contribute_to_class(self, cls, name):
            if func:
                func(self, cls, name)
            else:
                super(superclass, self).contribute_to_class(cls, name)
            setattr(cls, self.name, Creator(self))

        return contribute_to_class


    from django.db.models.query import QuerySet
    from django.utils import six, timezone
    from django.utils.encoding import force_text
    from django.utils.functional import Promise
    import datetime, decimal, json, uuid

    class JSONEncoder(json.JSONEncoder):
        __doc__ = '\n        JSONEncoder subclass that knows how to encode date/time/timedelta,\n        decimal types, generators and other basic python objects.\n        Taken from https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/utils/encoders.py\n        '

        def default(self, obj):
            if isinstance(obj, Promise):
                return force_text(obj)
            else:
                if isinstance(obj, datetime.datetime):
                    representation = obj.isoformat()
                    if obj.microsecond:
                        representation = representation[:23] + representation[26:]
                    if representation.endswith('+00:00'):
                        representation = representation[:-6] + 'Z'
                    return representation
                elif isinstance(obj, datetime.date):
                    return obj.isoformat()
                else:
                    if isinstance(obj, datetime.time):
                        if timezone:
                            if timezone.is_aware(obj):
                                raise ValueError("JSON can't represent timezone-aware times.")
                            representation = obj.isoformat()
                            if obj.microsecond:
                                representation = representation[:12]
                            return representation
                        elif isinstance(obj, datetime.timedelta):
                            return six.text_type(obj.total_seconds())
                        if isinstance(obj, decimal.Decimal):
                            return float(obj)
                        if isinstance(obj, uuid.UUID):
                            return six.text_type(obj)
                    else:
                        if isinstance(obj, QuerySet):
                            return tuple(obj)
                        if hasattr(obj, 'tolist'):
                            return obj.tolist()
                    if hasattr(obj, '__getitem__'):
                        try:
                            return dict(obj)
                        except:
                            pass

                    elif hasattr(obj, '__iter__'):
                        return tuple(item for item in obj)
                return super(JSONEncoder, self).default(obj)


    class JSONFormFieldBase(object):

        def __init__(self, *args, **kwargs):
            self.load_kwargs = kwargs.pop('load_kwargs', {})
            (super(JSONFormFieldBase, self).__init__)(*args, **kwargs)

        def to_python(self, value):
            if isinstance(value, six.string_types):
                if value:
                    try:
                        return (json.loads)(value, **self.load_kwargs)
                    except ValueError:
                        raise ValidationError(_('Enter valid JSON'))

            return value

        def clean(self, value):
            if not value:
                if not self.required:
                    return
            try:
                return super(JSONFormFieldBase, self).clean(value)
            except TypeError:
                raise ValidationError(_('Enter valid JSON'))


    class JSONFormField(JSONFormFieldBase, fields.CharField):
        pass


    class JSONCharFormField(JSONFormFieldBase, fields.CharField):
        pass


    class JSONFieldBase(six.with_metaclass(SubfieldBase, models.Field)):

        def __init__(self, *args, **kwargs):
            self.dump_kwargs = kwargs.pop('dump_kwargs', {'cls':JSONEncoder, 
             'separators':(',', ':')})
            self.load_kwargs = kwargs.pop('load_kwargs', {})
            (super(JSONFieldBase, self).__init__)(*args, **kwargs)

        def pre_init(self, value, obj):
            """Convert a string value to JSON only if it needs to be deserialized.

            SubfieldBase metaclass has been modified to call this method instead of
            to_python so that we can check the obj state and determine if it needs to be
            deserialized"""
            try:
                if obj._state.adding:
                    if getattr(obj, 'pk', None) is not None:
                        if isinstance(value, six.string_types):
                            try:
                                return (json.loads)(value, **self.load_kwargs)
                            except ValueError:
                                raise ValidationError(_('Enter valid JSON'))

            except AttributeError:
                pass

            return value

        def to_python(self, value):
            """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
            is still necessary for Django's deserializer"""
            return value

        def get_prep_value(self, value):
            """Convert JSON object to a string"""
            if self.null:
                if value is None:
                    return
            return (json.dumps)(value, **self.dump_kwargs)

        def value_to_string(self, obj):
            value = self.value_from_object(obj, dump=False)
            return self.get_db_prep_value(value, None)

        def value_from_object(self, obj, dump=True):
            value = super(JSONFieldBase, self).value_from_object(obj)
            if self.null:
                if value is None:
                    return
            if dump:
                return self.dumps_for_display(value)
            else:
                return value

        def dumps_for_display(self, value):
            return (json.dumps)(value, **self.dump_kwargs)

        def formfield(self, **kwargs):
            if 'form_class' not in kwargs:
                kwargs['form_class'] = self.form_class
            else:
                field = (super(JSONFieldBase, self).formfield)(**kwargs)
                if isinstance(field, JSONFormFieldBase):
                    field.load_kwargs = self.load_kwargs
                field.help_text = field.help_text or 'Enter valid JSON'
            return field

        def get_default(self):
            if self.has_default():
                if callable(self.default):
                    return self.default()
                return copy.deepcopy(self.default)
            else:
                return super(JSONFieldBase, self).get_default()


    class JSONField(JSONFieldBase, models.TextField):
        __doc__ = 'JSONField is a generic textfield that serializes/deserializes JSON objects'
        form_class = JSONFormField

        def dumps_for_display(self, value):
            kwargs = {'indent': 2}
            kwargs.update(self.dump_kwargs)
            return (json.dumps)(value, ensure_ascii=False, **kwargs)


    class JSONCharField(JSONFieldBase, models.CharField):
        __doc__ = 'JSONCharField is a generic textfield that serializes/deserializes JSON objects,\n        stored in the database like a CharField, which enables it to be used\n        e.g. in unique keys'
        form_class = JSONCharFormField


    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ['^jsonfield\\.fields\\.(JSONField|JSONCharField)'])
    except ImportError:
        pass

__all__ = ['JSONField']