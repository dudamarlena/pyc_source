# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/foreignkey.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.conf import settings
from django.db.models import ForeignKey
__all__ = ('FlexibleForeignKey', )

class FlexibleForeignKey(ForeignKey):

    def db_type(self, connection):
        rel_field = self.related_field
        if hasattr(rel_field, 'get_related_db_type'):
            return rel_field.get_related_db_type(connection)
        return super(FlexibleForeignKey, self).db_type(connection)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [
     '^sentry\\.db\\.models\\.fields\\.FlexibleForeignKey',
     '^sentry\\.db\\.models\\.fields\\.foreignkey\\.FlexibleForeignKey'])