# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0003_auto_20160914_1821.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1002 bytes
from django.db import migrations
import django.db.models.deletion, djangoplus.admin.models, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('admin', '0002_log_logindex')]
    operations = [
     migrations.CreateModel(name='ContentType',
       fields=[],
       options={'proxy': True},
       bases=('contenttypes.contenttype', ),
       managers=[
      (
       'objects', djangoplus.admin.models.ContentTypeManager())]),
     migrations.AlterField(model_name='log',
       name='content_type',
       field=djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='admin.ContentType', verbose_name='Objeto'))]