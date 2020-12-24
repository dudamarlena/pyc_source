# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/pickle.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.conf import settings
from picklefield.fields import PickledObjectField

class UnicodePickledObjectField(PickledObjectField):

    def get_db_prep_value(self, value, *args, **kwargs):
        if isinstance(value, six.binary_type):
            value = value.decode('utf-8')
        return super(UnicodePickledObjectField, self).get_db_prep_value(value, *args, **kwargs)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^sentry\\.db\\.models\\.fields\\.pickle\\.UnicodePickledObjectField'])