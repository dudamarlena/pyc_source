# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/citext.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import six
from django.conf import settings
from django.db import connections, models
from django.db.models.signals import pre_migrate
__all__ = ('CITextField', 'CICharField', 'CIEmailField')

class CIText(object):

    def db_type(self, connection):
        engine = connection.settings_dict['ENGINE']
        if 'postgres' in engine:
            return 'citext'
        return super(CIText, self).db_type(connection)


class CITextField(CIText, models.TextField):
    pass


class CICharField(CIText, models.CharField):
    pass


class CIEmailField(CIText, models.EmailField):
    pass


if hasattr(models, 'SubfieldBase'):
    CITextField = six.add_metaclass(models.SubfieldBase)(CITextField)
    CICharField = six.add_metaclass(models.SubfieldBase)(CICharField)
    CIEmailField = six.add_metaclass(models.SubfieldBase)(CIEmailField)
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^sentry\\.db\\.models\\.fields\\.citext\\.CITextField'])
    add_introspection_rules([], ['^sentry\\.db\\.models\\.fields\\.citext\\.CICharField'])
    add_introspection_rules([], ['^sentry\\.db\\.models\\.fields\\.citext\\.CIEmailField'])

def create_citext_extension(using, **kwargs):
    from sentry.utils.db import is_postgres
    if is_postgres(using):
        cursor = connections[using].cursor()
        try:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS citext')
        except Exception:
            pass


pre_migrate.connect(create_citext_extension)