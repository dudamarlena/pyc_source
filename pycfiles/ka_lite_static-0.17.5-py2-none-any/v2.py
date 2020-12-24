# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/v2.py
# Compiled at: 2018-07-11 18:15:31
"""
API versioning file; we can tell what kind of migrations things are
by what class they inherit from (if none, it's a v1).
"""
from south.utils import ask_for_it_by_name

class BaseMigration(object):

    def gf(self, field_name):
        """Gets a field by absolute reference."""
        field = ask_for_it_by_name(field_name)
        field.model = FakeModel
        return field


class SchemaMigration(BaseMigration):
    pass


class DataMigration(BaseMigration):
    no_dry_run = True


class FakeModel(object):
    """Fake model so error messages on fields don't explode"""
    pass