# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/serializers/base.py
# Compiled at: 2012-12-04 06:13:21
try:
    from collections import OrderedDict
except ImportError:
    from ..lib.ordereddict import OrderedDict

import django.db.models, django.core.files, django.forms, datetime
from decimal import Decimal

class Serializer(object):
    """Base class for serializers."""

    def __init__(self, source):
        self.source = source

    def serialize(self, request):
        """
        Serialize the given object into into simple
        data types (e.g. lists, dictionaries, strings).
        """

        def serialize(anything):

            def serialize_dictionary(dictionary):
                """Dictionaries are serialized recursively."""
                data = OrderedDict()
                for key, value in dictionary.items():
                    data.update({key: serialize(value)})

                return data

            def serialize_list(list):
                """Lists are serialized recursively."""
                data = []
                for item in list:
                    data.append(serialize(item))

                return data

            def serialize_queryset(queryset):
                """Querysets are serialized as lists of models."""
                data = []
                for model in queryset:
                    data.append(serialize_model(model))

                return data

            def serialize_datequeryset(datequeryset):
                """DateQuerysets are serialized as lists of dates."""
                data = []
                for date in datequeryset:
                    data.append(serialize_date(date))

                return data

            def serialize_valueslistqueryset(valueslistqueryset):
                """DateQuerysets are serialized as lists of values."""
                data = []
                for value in valueslistqueryset:
                    if isinstance(value, tuple):
                        data.append(serialize_list(value))
                    else:
                        data.append(serialize(value))

                return data

            def serialize_manager(manager):
                """Managers are serialized as list of models."""
                data = []
                for model in manager.all():
                    data.append(serialize_model(model))

                return data

            def serialize_model(model):
                """
                Models are serialized by calling their 'serialize' method.

                Models that don't define a 'serialize' method are
                serialized as a dictionary of fields.

                Example:

                    {
                        'id': 1,
                        'title': 'Mmmm pie',
                        'content: 'Pie is good!'
                    }

                """
                if hasattr(model, 'serialize'):
                    return serialize(model.serialize())
                else:
                    data = OrderedDict()
                    for field in model._meta.fields + model._meta.many_to_many:
                        data.update({field.name: serialize(getattr(model, field.name))})

                    return data

            def serialize_form(form):
                """
                Forms are serialized as a dictionary of fields and errors (if any).

                Example:

                    {
                        'fields': ['title', 'content'],
                        'errors': {
                            'content': 'Must describe pie.'
                        }
                    }

                """
                data = OrderedDict()
                data['fields'] = []
                for field in form.fields:
                    data['fields'].append(field)

                if form.errors:
                    data['errors'] = []
                    for field in form:
                        data['errors'].append({'field': field.name, 
                           'error': field.errors.as_text()})

                return data

            def serialize_date(datetime):
                """Dates are serialized as ISO 8601-compatible strings."""
                return datetime.isoformat()

            def serialize_field_file(field_file):
                """Filefields are serialized as strings describing their URL."""
                try:
                    return field_file.url
                except ValueError:
                    return

                return

            def serialize_image_field_file(image_field_file):
                """Imagefields are serialized as strings describing their URL."""
                try:
                    return image_field_file.url
                except ValueError:
                    return

                return

            def serialize_decimal_field(decimal_field):
                """Decimal fields are serialized as strings."""
                try:
                    return str(decimal_field)
                except ValueError:
                    return

                return

            if isinstance(anything, dict):
                return serialize_dictionary(anything)
            else:
                if isinstance(anything, (list, set)):
                    return serialize_list(anything)
                if isinstance(anything, django.db.models.query.DateQuerySet):
                    return serialize_datequeryset(anything)
                if isinstance(anything, django.db.models.query.ValuesListQuerySet):
                    return serialize_valueslistqueryset(anything)
                if isinstance(anything, django.db.models.query.QuerySet):
                    return serialize_queryset(anything)
                if isinstance(anything, django.db.models.Model):
                    return serialize_model(anything)
                if isinstance(anything, (django.forms.Form, django.forms.ModelForm)):
                    return serialize_form(anything)
                if isinstance(anything, (str, unicode)):
                    return anything
                if isinstance(anything, (int, float, long)):
                    return anything
                if isinstance(anything, (datetime.date, datetime.datetime)):
                    return serialize_date(anything)
                if isinstance(anything, django.db.models.manager.Manager):
                    return serialize_manager(anything)
                if isinstance(anything, Decimal):
                    return serialize_decimal_field(anything)
                if isinstance(anything, django.core.files.base.File):
                    return serialize_field_file(anything)
                if anything is None:
                    return
                if hasattr(anything, 'serialize'):
                    return serialize(anything.serialize())
                raise TypeError("Respite doesn't know how to serialize %s" % anything.__class__.__name__)
                return

        return serialize(self.source)