# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/studygroups/migrations/0002_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 683 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('studygroups', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='studygroup',
       name='header_image',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), to='pages.HeaderImage', null=True)),
     migrations.AlterField(model_name='studygroup',
       name='meta',
       field=models.OneToOneField(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='meta.Meta'))]