# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0021_auto_20171218_1039.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 936 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix', '0020_remotelog')]
    operations = [
     migrations.AddField(model_name='log', name='username', field=models.CharField(blank=True, default='', max_length=200, verbose_name='Username')),
     migrations.AddField(model_name='remotelog', name='username', field=models.CharField(blank=True, default='', max_length=200, verbose_name='Username')),
     migrations.AlterField(model_name='remotelog', name='user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL))]