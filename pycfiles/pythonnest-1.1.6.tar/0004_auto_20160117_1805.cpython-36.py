# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/migrations/0004_auto_20160117_1805.py
# Compiled at: 2018-04-21 03:59:37
# Size of source mod 2**32: 5011 bytes
from django.db import migrations, models
import pythonnest.models

class Migration(migrations.Migration):
    dependencies = [
     ('pythonnest', '0003_auto_20160105_2338')]
    operations = [
     migrations.AlterField(model_name='classifier',
       name='name',
       field=models.CharField(db_index=True, max_length=455, verbose_name='Classifier')),
     migrations.AlterField(model_name='dependence',
       name='name',
       field=models.CharField(db_index=True, max_length=455, verbose_name='Classifier')),
     migrations.AlterField(model_name='log',
       name='action',
       field=models.CharField(blank=True, default='', max_length=455, verbose_name='action')),
     migrations.AlterField(model_name='package',
       name='author',
       field=models.CharField(blank=True, db_index=True, max_length=455, null=True, verbose_name='author')),
     migrations.AlterField(model_name='package',
       name='author_email',
       field=models.CharField(blank=True, db_index=True, max_length=455, null=True, verbose_name='author email')),
     migrations.AlterField(model_name='package',
       name='license',
       field=models.CharField(blank=True, db_index=True, default='UNKNOWN', max_length=455, verbose_name='license')),
     migrations.AlterField(model_name='package',
       name='maintainer',
       field=models.CharField(blank=True, db_index=True, max_length=455, null=True, verbose_name='maintainer')),
     migrations.AlterField(model_name='package',
       name='maintainer_email',
       field=models.CharField(blank=True, db_index=True, max_length=455, null=True, verbose_name='maintainer email')),
     migrations.AlterField(model_name='package',
       name='name',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, verbose_name='package name')),
     migrations.AlterField(model_name='package',
       name='normalized_name',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, verbose_name='normalized name')),
     migrations.AlterField(model_name='packagetype',
       name='name',
       field=models.CharField(db_index=True, max_length=455, verbose_name='Classifier')),
     migrations.AlterField(model_name='release',
       name='keywords',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, null=True, verbose_name='keywords')),
     migrations.AlterField(model_name='release',
       name='stable_version',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, null=True, verbose_name='stable version name')),
     migrations.AlterField(model_name='release',
       name='version',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, null=True, verbose_name='version name')),
     migrations.AlterField(model_name='releasedownload',
       name='file',
       field=models.FileField(db_index=True, max_length=455, upload_to=(pythonnest.models.release_download_path), verbose_name='File')),
     migrations.AlterField(model_name='releasedownload',
       name='filename',
       field=models.CharField(db_index=True, max_length=455, verbose_name='Filename')),
     migrations.AlterField(model_name='releasedownload',
       name='python_version',
       field=models.CharField(blank=True, db_index=True, default='any', max_length=355, verbose_name='Python version')),
     migrations.AlterField(model_name='releasedownload',
       name='url',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, verbose_name='URL')),
     migrations.AlterField(model_name='synchronization',
       name='destination',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, verbose_name='Destination')),
     migrations.AlterField(model_name='synchronization',
       name='source',
       field=models.CharField(blank=True, db_index=True, default='', max_length=455, verbose_name='Source'))]