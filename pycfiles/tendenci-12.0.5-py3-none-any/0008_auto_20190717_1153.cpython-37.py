# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/migrations/0008_auto_20190717_1153.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 833 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('forums', '0007_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='post',
       name='user',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='posts', to=(settings.AUTH_USER_MODEL), verbose_name='User')),
     migrations.AlterField(model_name='topic',
       name='user',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), verbose_name='Owner'))]