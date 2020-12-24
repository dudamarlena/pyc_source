# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/migrations/0001_initial.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('jmbo', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'DummyModel', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase')),
      (
       b'test_editable_field', models.CharField(max_length=32)),
      (
       b'test_non_editable_field', models.CharField(editable=False, max_length=32))], options={b'abstract': False}, bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'DummyRelationalModel1', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID'))]),
     migrations.CreateModel(name=b'DummyRelationalModel2', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID'))]),
     migrations.CreateModel(name=b'DummySourceModelBase', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase')),
      (
       b'points_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'tests.DummyModel')),
      (
       b'points_to_many', models.ManyToManyField(related_name=b'to_many', to=b'tests.DummyModel'))], options={b'abstract': False}, bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'DummyTargetModelBase', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase'))], options={b'abstract': False}, bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'TestModel', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase')),
      (
       b'content', models.CharField(max_length=255, null=True, blank=True))], options={b'abstract': False}, bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'TrunkModel', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase'))], options={b'abstract': False}, bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'BranchModel', fields=[
      (
       b'trunkmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'tests.TrunkModel'))], options={b'abstract': False}, bases=('tests.trunkmodel', )),
     migrations.AddField(model_name=b'dummymodel', name=b'test_foreign_field', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'tests.DummyRelationalModel1')),
     migrations.AddField(model_name=b'dummymodel', name=b'test_foreign_published', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'foreign_published', to=b'tests.DummyTargetModelBase')),
     migrations.AddField(model_name=b'dummymodel', name=b'test_foreign_unpublished', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'foreign_unpublished', to=b'tests.DummyTargetModelBase')),
     migrations.AddField(model_name=b'dummymodel', name=b'test_many_field', field=models.ManyToManyField(to=b'tests.DummyRelationalModel2')),
     migrations.AddField(model_name=b'dummymodel', name=b'test_many_published', field=models.ManyToManyField(blank=True, null=True, related_name=b'many_published', to=b'tests.DummyTargetModelBase')),
     migrations.AddField(model_name=b'dummymodel', name=b'test_many_unpublished', field=models.ManyToManyField(blank=True, null=True, related_name=b'many_unpublished', to=b'tests.DummyTargetModelBase')),
     migrations.CreateModel(name=b'LeafModel', fields=[
      (
       b'branchmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'tests.BranchModel'))], options={b'abstract': False}, bases=('tests.branchmodel', ))]