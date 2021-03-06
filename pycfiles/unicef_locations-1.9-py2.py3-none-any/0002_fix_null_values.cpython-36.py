# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0002_fix_null_values.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 947 bytes
from django.db import migrations

def fix_null_values(model, field_names, new_value=''):
    """
    For each fieldname, update any records in 'model' where the field's value is NULL
    to be an empty string instead (or whatever new_value is)
    """
    for name in field_names:
        ((model._default_manager.filter)(**{name: None}).update)(**{name: new_value})


def fix_nulls(apps, schema):
    fix_null_values(apps.get_model('locations.cartodbtable'), [
     'color',
     'display_name',
     'parent_code_col'])
    fix_null_values(apps.get_model('locations.location'), [
     'p_code'])


class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0001_initial')]
    operations = [
     migrations.RunPython(fix_nulls, migrations.RunPython.noop)]