# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0003_auto_20181026_1745.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1681 bytes
import aparnik.utils.utils
from django.db import migrations, models
import s3direct.fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0002_auto_20181025_1617')]
    operations = [
     migrations.AlterModelOptions(name='filefield',
       options={'verbose_name':'\\u0641\\u0627\\u06cc\\u0644 \\u0641\\u06cc\\u0644\\u062f', 
      'verbose_name_plural':'\\u0641\\u0627\\u06cc\\u0644 \\u0641\\u06cc\\u0644\\u062f'}),
     migrations.AlterField(model_name='filefield',
       name='file_direct',
       field=models.FileField(blank=True, null=True, upload_to=(aparnik.utils.utils.document_directory_path), verbose_name='\\u0641\\u0627\\u06cc\\u0644')),
     migrations.AlterField(model_name='filefield',
       name='file_s3',
       field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='\\u0641\\u0627\\u06cc\\u0644')),
     migrations.AlterField(model_name='filefield',
       name='size',
       field=models.IntegerField(default=0, verbose_name='\\u0633\\u0627\\u06cc\\u0632 \\u0641\\u0627\\u06cc\\u0644')),
     migrations.AlterField(model_name='filefield',
       name='type',
       field=models.CharField(choices=[('M', '\\u0641\\u06cc\\u0644\\u0645'), ('V', '\\u0635\\u062f\\u0627'), ('P', '\\u067e\\u06cc \\u062f\\u06cc \\u0627\\u0641'), ('I', '\\u0639\\u06a9\\u0633')], max_length=1, verbose_name='\\u0646\\u0648\\u0639 \\u0641\\u0627\\u06cc\\u0644'))]