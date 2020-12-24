# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/gzippeddict.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import logging, six
from django.conf import settings
from django.db.models import TextField
from sentry.db.models.utils import Creator
from sentry.utils.compat import pickle
from sentry.utils.strings import decompress, compress
__all__ = ('GzippedDictField', )
logger = logging.getLogger('sentry')

class GzippedDictField(TextField):
    """
    Slightly different from a JSONField in the sense that the default
    value is a dictionary.
    """

    def contribute_to_class(self, cls, name):
        """
        Add a descriptor for backwards compatibility
        with previous Django behavior.
        """
        super(GzippedDictField, self).contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

    def to_python(self, value):
        if isinstance(value, six.string_types) and value:
            try:
                value = pickle.loads(decompress(value))
            except Exception as e:
                logger.exception(e)
                return {}

        elif not value:
            return {}
        return value

    def get_prep_value(self, value):
        if not value and self.null:
            return None
        else:
            if isinstance(value, six.binary_type):
                value = six.text_type(value)
            return compress(pickle.dumps(value))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^sentry\\.db\\.models\\.fields\\.gzippeddict\\.GzippedDictField'])