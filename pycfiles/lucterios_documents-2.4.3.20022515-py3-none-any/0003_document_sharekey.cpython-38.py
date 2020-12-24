# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-documents/lucterios/documents/migrations/0003_document_sharekey.py
# Compiled at: 2019-10-15 08:48:27
# Size of source mod 2**32: 420 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('documents', '0002_length_name')]
    operations = [
     migrations.AddField(model_name='document',
       name='sharekey',
       field=models.CharField(max_length=100, null=True, verbose_name='sharekey'))]