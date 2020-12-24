# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/migrations/0004_auto_20190708_1832.py
# Compiled at: 2020-05-05 22:21:28
# Size of source mod 2**32: 1064 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_admin_settings', '0003_menu')]
    operations = [
     migrations.AlterField(model_name='menu',
       name='content_type',
       field=models.ForeignKey(blank=True, help_text='use for permission control.', null=True, on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType', verbose_name='ContentType')),
     migrations.AlterField(model_name='menu',
       name='link',
       field=models.CharField(blank=True, help_text='support admin:index or /admin/ or http://', max_length=255, null=True, verbose_name='Link')),
     migrations.AlterField(model_name='menu',
       name='link_type',
       field=models.IntegerField(choices=[(0, 'Internal'), (1, 'External'), (3, 'Divide')], default=0, verbose_name='Link Type'))]