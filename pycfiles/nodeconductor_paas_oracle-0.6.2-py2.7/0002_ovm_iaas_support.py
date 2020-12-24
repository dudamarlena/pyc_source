# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/migrations/0002_ovm_iaas_support.py
# Compiled at: 2016-12-16 07:39:01
from __future__ import unicode_literals
from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_paas_oracle', '0001_squashed_0007_change_support_requests')]
    operations = [
     migrations.AlterField(model_name=b'deployment', name=b'db_arch_size', field=models.PositiveIntegerField(blank=True, help_text=b'Archive storage size in GB', null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(2048)])),
     migrations.AlterField(model_name=b'deployment', name=b'db_charset', field=models.CharField(blank=True, max_length=256, choices=[('AL32UTF8 - Unicode UTF-8 Universal Character Set', 'AL32UTF8 - Unicode UTF-8 Universal Character Set'), ('AR8ISO8859P6 - ISO 8859-6 Latin/Arabic', 'AR8ISO8859P6 - ISO 8859-6 Latin/Arabic'), ('AR8MSWIN1256 - MS Windows Code Page 1256 8-Bit Latin/Arabic', 'AR8MSWIN1256 - MS Windows Code Page 1256 8-Bit Latin/Arabic'), ('Other - please specify in Addtional Data field.', 'Other - please specify in Addtional Data field.')])),
     migrations.AlterField(model_name=b'deployment', name=b'db_template', field=models.CharField(blank=True, max_length=256, choices=[('General Purpose', 'General Purpose'), ('Data Warehouse', 'Data Warehouse')])),
     migrations.AlterField(model_name=b'deployment', name=b'db_type', field=models.PositiveSmallIntegerField(choices=[(1, 'RAC'), (2, 'Single Instance/ASM'), (3, 'Single Instance'), (4, 'No database')])),
     migrations.AlterField(model_name=b'deployment', name=b'db_version', field=models.CharField(blank=True, max_length=256, choices=[('11.2.0.4', '11.2.0.4'), ('12.1.0.2', '12.1.0.2')]))]