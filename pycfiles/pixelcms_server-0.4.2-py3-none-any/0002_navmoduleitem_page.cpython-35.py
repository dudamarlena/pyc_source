# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/nav/migrations/0002_navmoduleitem_page.py
# Compiled at: 2016-10-22 17:11:10
# Size of source mod 2**32: 619 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('nav', '0001_initial'),
     ('pages', '0001_initial')]
    operations = [
     migrations.AddField(model_name='navmoduleitem', name='page', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Page', verbose_name='page'))]