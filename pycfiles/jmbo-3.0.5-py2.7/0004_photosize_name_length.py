# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0004_photosize_name_length.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import migrations, models
from django.utils import timezone

def fix_app_label(apps, schema_editor):
    migrations.recorder.MigrationRecorder.Migration.objects.create(app=b'jmbo', name=b'0004_photosize_name_length', applied=timezone.now())


class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0003_auto_20160530_1247')]
    operations = [
     migrations.AlterField(model_name=b'photosize', name=b'name', field=models.CharField(unique=True, max_length=255, validators=[RegexValidator(regex=b'^[a-z0-9_]+$', message=b'Use only plain lowercase letters (ASCII), numbers and underscores.')])),
     migrations.RunPython(fix_app_label)]

    def __init__(self, *args, **kwargs):
        super(Migration, self).__init__(*args, **kwargs)
        self.app_label = b'photologue'