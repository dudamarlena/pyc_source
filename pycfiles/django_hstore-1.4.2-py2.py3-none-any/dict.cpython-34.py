# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/dict.py
# Compiled at: 2016-04-01 11:33:40
# Size of source mod 2**32: 5377 bytes
import json
from decimal import Decimal
from django.utils import six
from django.utils.encoding import force_text, force_str
from .compat import UnicodeMixin
from . import utils, exceptions
__all__ = [
 'HStoreDict',
 'HStoreReferenceDict']

class DecimalEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class HStoreDict(UnicodeMixin, dict):
    __doc__ = '\n    A dictionary subclass which implements hstore support.\n    '
    schema_mode = False

    def __init__(self, value=None, field=None, instance=None, schema_mode=False, **kwargs):
        self.schema_mode = schema_mode
        if isinstance(value, six.string_types):
            try:
                value = json.loads(value)
            except ValueError as e:
                raise exceptions.HStoreDictException('HStoreDict accepts only valid json formatted strings.', json_error_message=force_text(e))

        else:
            if value is None:
                value = {}
            if not isinstance(value, dict):
                raise exceptions.HStoreDictException('HStoreDict accepts only dictionary objects, None and json formatted string representations of json objects')
            if not self.schema_mode:
                for key, val in value.items():
                    value[key] = self.ensure_acceptable_value(val)

            super(HStoreDict, self).__init__(value, **kwargs)
            self.field = field
            self.instance = instance

    def __setitem__(self, *args, **kwargs):
        """
        perform checks before setting the value of a key
        """
        value = self.ensure_acceptable_value(args[1])
        args = (
         args[0], value)
        super(HStoreDict, self).__setitem__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        """
        retrieve value preserving type if in schema mode, string only otherwise
        """
        value = super(HStoreDict, self).__getitem__(*args, **kwargs)
        if self.schema_mode:
            try:
                return self.instance._hstore_virtual_fields[args[0]].to_python(value)
            except KeyError:
                pass

        return value

    def get(self, *args):
        key = args[0]
        try:
            return self.__getitem__(key)
        except KeyError:
            if len(args) > 1:
                return args[1]
            else:
                return

    def __unicode__(self):
        return force_text(json.dumps(self))

    def __getstate__(self):
        return self.__dict__

    def __copy__(self):
        return self.__class__(self, self.field)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def ensure_acceptable_value(self, value):
        """
        if schema_mode disabled (default behaviour):
            - ensure booleans, integers, floats, Decimals, lists and dicts are
              converted to string
            - convert True and False objects to "true" and "false" so they can be
              decoded back with the json library if needed
            - convert lists and dictionaries to json formatted strings
            - leave alone all other objects because they might be representation of django models
        else:
            - encode utf8 strings in python2
            - convert to string
        """
        if not self.schema_mode:
            if isinstance(value, bool):
                return force_text(value).lower()
            else:
                if isinstance(value, six.integer_types + (float, Decimal)):
                    return force_text(value)
                if isinstance(value, (list, dict)):
                    return force_text(json.dumps(value, cls=DecimalEncoder))
                return value
        else:
            if value is not None:
                value = force_str(value)
            return value

    def remove(self, keys):
        """
        Removes the specified keys from this dictionary.
        """
        queryset = self.instance._base_manager.get_query_set()
        queryset.filter(pk=self.instance.pk).hremove(self.field.name, keys)


class HStoreReferenceDict(HStoreDict):
    __doc__ = '\n    A dictionary which adds support to storing references to models\n    '

    def __getitem__(self, *args, **kwargs):
        value = super(self.__class__, self).__getitem__(*args, **kwargs)
        if isinstance(value, six.string_types):
            reference = utils.acquire_reference(value)
            self.__setitem__(args[0], reference)
            return reference
        return value

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default