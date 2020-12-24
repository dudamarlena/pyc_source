# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dodi/envs/isdc/isdc_modules/isdc_geodb/geodb/migrations/0002_auto_20181128_1016.py
# Compiled at: 2018-11-28 05:16:01
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('geodb', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Forcastedvalue', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'datadate', models.DateTimeField()),
      (
       b'forecasttype', models.CharField(max_length=50)),
      (
       b'riskstate', models.IntegerField()),
      (
       b'basin', models.ForeignKey(related_name=b'basins', to=b'geodb.AfgShedaLvl4'))], options={b'db_table': b'forcastedvalue', 
        b'managed': True}),
     migrations.CreateModel(name=b'forecastedLastUpdate', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'datadate', models.DateTimeField()),
      (
       b'forecasttype', models.CharField(max_length=50))], options={b'db_table': b'forecastedlastupdate', 
        b'managed': True}),
     migrations.RemoveField(model_name=b'afgavsa', name=b'basinmember'),
     migrations.DeleteModel(name=b'AfgEqHzda'),
     migrations.DeleteModel(name=b'AfgEqtUnkPplEqHzd'),
     migrations.DeleteModel(name=b'AfgIncidentOasis'),
     migrations.DeleteModel(name=b'AfgIncidentOasisTemp'),
     migrations.DeleteModel(name=b'AfgMettClim1KmChelsaBioclim'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc26'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc45'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc85'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc26'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc45'),
     migrations.DeleteModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc85'),
     migrations.DeleteModel(name=b'AfgMettClimperc1KmChelsaPrec'),
     migrations.DeleteModel(name=b'AfgMettClimtemp1KmChelsaTempavg'),
     migrations.DeleteModel(name=b'AfgMettClimtemp1KmChelsaTempmax'),
     migrations.DeleteModel(name=b'AfgMettClimtemp1KmChelsaTempmin'),
     migrations.DeleteModel(name=b'AfgSnowaAverageExtent'),
     migrations.DeleteModel(name=b'earthquake_events'),
     migrations.DeleteModel(name=b'earthquake_shakemap'),
     migrations.DeleteModel(name=b'HistoryDrought'),
     migrations.DeleteModel(name=b'RefSecurity'),
     migrations.DeleteModel(name=b'villagesummaryEQ'),
     migrations.DeleteModel(name=b'AfgAvsa')]