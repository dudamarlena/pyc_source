# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0011_auto_20181001_1853.py
# Compiled at: 2018-10-01 14:53:04
# Size of source mod 2**32: 1049 bytes
import django.core.validators
from django.db import migrations, models
import reader.validators

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0010_cachedimage')]
    operations = [
     migrations.AlterField(model_name='article',
       name='uri',
       field=models.URLField(max_length=2048)),
     migrations.AlterField(model_name='attachment',
       name='uri',
       field=models.URLField(max_length=2048)),
     migrations.AlterField(model_name='cachedimage',
       name='uri',
       field=models.URLField(db_index=True, max_length=2048, unique=True)),
     migrations.AlterField(model_name='feed',
       name='uri',
       field=models.URLField(max_length=2048, unique=True, validators=[django.core.validators.URLValidator(schemes=['http', 'https']), reader.validators.http_port_validator]))]