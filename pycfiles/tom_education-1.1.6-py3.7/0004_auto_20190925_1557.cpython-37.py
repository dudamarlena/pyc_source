# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/migrations/0004_auto_20190925_1557.py
# Compiled at: 2019-10-01 09:52:31
# Size of source mod 2**32: 1196 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('tom_dataproducts', '0006_auto_20190912_2013'),
     ('tom_education', '0003_asyncprocess_process_type')]
    operations = [
     migrations.RemoveField(model_name='timelapseprocess',
       name='asyncprocess_ptr'),
     migrations.RemoveField(model_name='timelapseprocess',
       name='timelapse_product'),
     migrations.CreateModel(name='TimelapsePipeline',
       fields=[],
       options={'proxy':True, 
      'indexes':[],  'constraints':[]},
       bases=('tom_education.pipelineprocess', )),
     migrations.AlterField(model_name='asyncprocess',
       name='identifier',
       field=models.CharField(max_length=100, unique=True)),
     migrations.DeleteModel(name='TimelapseDataProduct'),
     migrations.DeleteModel(name='TimelapseProcess')]