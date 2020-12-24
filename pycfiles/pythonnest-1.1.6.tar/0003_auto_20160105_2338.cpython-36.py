# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/migrations/0003_auto_20160105_2338.py
# Compiled at: 2018-04-21 03:59:37
# Size of source mod 2**32: 2682 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pythonnest', '0002_auto_20141005_2218')]
    operations = [
     migrations.AlterField(model_name='release',
       name='classifiers',
       field=models.ManyToManyField(blank=True, db_index=True, to='pythonnest.Classifier')),
     migrations.AlterField(model_name='release',
       name='obsoletes',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_obsoletes', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='obsoletes_dist',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_obsoletes_dist', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='provides',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_provides', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='provides_dist',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_provides_dist', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='requires',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_requires', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='requires_dist',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_requires_dist', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='requires_external',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_requires_external', to='pythonnest.Dependence')),
     migrations.AlterField(model_name='release',
       name='requires_python',
       field=models.ManyToManyField(blank=True, db_index=True, related_name='dep_requires_python', to='pythonnest.Dependence'))]