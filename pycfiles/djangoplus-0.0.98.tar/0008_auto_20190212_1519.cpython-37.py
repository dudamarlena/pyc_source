# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0008_auto_20190212_1519.py
# Compiled at: 2019-02-12 14:18:06
# Size of source mod 2**32: 782 bytes
from django.db import migrations

def migrate(apps, schema):
    for model in apps.get_models():
        for field in model._meta.fields:
            if field.__class__.__name__ == 'ImageField':
                default = field.default
                if default and type(default) in (bytes, str) and type(default) == bytes:
                    default = default.decode()
                    ((model.objects.filter)(**{'{}__contains'.format(field.name): '/static/'}).update)(**{field.name: default.split('/')[(-1)]})


class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0007_auto_20180416_1854')]
    operations = [
     migrations.RunPython(migrate)]