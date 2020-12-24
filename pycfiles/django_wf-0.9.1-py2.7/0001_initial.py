# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_workflow/migrations/0001_initial.py
# Compiled at: 2017-08-29 03:30:51
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Callback', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'function_name', models.CharField(max_length=200, verbose_name=b'Name')),
      (
       b'function_module', models.CharField(max_length=400, verbose_name=b'Module')),
      (
       b'order', models.IntegerField(verbose_name=b'Order')),
      (
       b'execute_async', models.BooleanField(default=False, verbose_name=b'Execute Asynchronously'))], options={b'ordering': [
                    b'order']}),
     migrations.CreateModel(name=b'CallbackParameter', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=100, verbose_name=b'Name')),
      (
       b'value', models.CharField(max_length=4000, verbose_name=b'Value')),
      (
       b'callback', models.ForeignKey(verbose_name=b'Callback', to=b'django_workflow.Callback'))]),
     migrations.CreateModel(name=b'Condition', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'condition_type', models.CharField(max_length=10, verbose_name=b'Type', choices=[('function', 'Function Call'), ('and', 'Boolean AND'), ('or', 'Boolean OR'), ('not', 'Boolean NOT')])),
      (
       b'parent_condition', models.ForeignKey(related_name=b'child_conditions', verbose_name=b'Parent Condition', blank=True, to=b'django_workflow.Condition', null=True))]),
     migrations.CreateModel(name=b'CurrentObjectState', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'object_id', models.CharField(max_length=200, verbose_name=b'Object Id')),
      (
       b'updated_ts', models.DateTimeField(auto_now=True, verbose_name=b'Last Updated'))]),
     migrations.CreateModel(name=b'Function', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'function_name', models.CharField(max_length=200, verbose_name=b'Function')),
      (
       b'function_module', models.CharField(max_length=400, verbose_name=b'Module')),
      (
       b'condition', models.ForeignKey(verbose_name=b'Condition', to=b'django_workflow.Condition'))]),
     migrations.CreateModel(name=b'FunctionParameter', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=100, verbose_name=b'Name')),
      (
       b'value', models.CharField(max_length=4000, verbose_name=b'Value')),
      (
       b'function', models.ForeignKey(related_name=b'parameters', verbose_name=b'Function', to=b'django_workflow.Function'))]),
     migrations.CreateModel(name=b'State', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=200, verbose_name=b'Name')),
      (
       b'active', models.BooleanField(verbose_name=b'Active')),
      (
       b'initial', models.BooleanField(default=False, verbose_name=b'Initial'))]),
     migrations.CreateModel(name=b'Transition', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=200, null=True, verbose_name=b'Name', blank=True)),
      (
       b'priority', models.IntegerField(null=True, verbose_name=b'Priority', blank=True)),
      (
       b'automatic', models.BooleanField(verbose_name=b'Automatic')),
      (
       b'automatic_delay', models.FloatField(null=True, verbose_name=b'Automatic Delay in Days', blank=True)),
      (
       b'final_state', models.ForeignKey(related_name=b'incoming_transitions', verbose_name=b'Final State', to=b'django_workflow.State')),
      (
       b'initial_state', models.ForeignKey(related_name=b'outgoing_transitions', verbose_name=b'Initial State', to=b'django_workflow.State'))], options={b'ordering': [
                    b'priority']}),
     migrations.CreateModel(name=b'TransitionLog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'user_id', models.IntegerField(null=True, verbose_name=b'User Id', blank=True)),
      (
       b'object_id', models.IntegerField(verbose_name=b'Object Id')),
      (
       b'completed_ts', models.DateTimeField(auto_now=True, verbose_name=b'Time of Completion')),
      (
       b'success', models.BooleanField(verbose_name=b'Success')),
      (
       b'error_code', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'Error Code', choices=[('400', '400 - Not Authorized'), ('500', '500 - Internal Error')])),
      (
       b'error_message', models.CharField(max_length=4000, null=True, verbose_name=b'Error Message', blank=True)),
      (
       b'transition', models.ForeignKey(verbose_name=b'Transition', to=b'django_workflow.Transition'))]),
     migrations.CreateModel(name=b'Workflow', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(unique=True, max_length=200, verbose_name=b'Name')),
      (
       b'object_type', models.CharField(max_length=200, verbose_name=b'Object_Type'))]),
     migrations.AddField(model_name=b'transitionlog', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'transition', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'state', name=b'workflow', field=models.ForeignKey(verbose_name=b'Workflow', to=b'django_workflow.Workflow')),
     migrations.AddField(model_name=b'functionparameter', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'function', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'currentobjectstate', name=b'state', field=models.ForeignKey(verbose_name=b'State', to=b'django_workflow.State')),
     migrations.AddField(model_name=b'currentobjectstate', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'condition', name=b'transition', field=models.ForeignKey(verbose_name=b'Transition', blank=True, to=b'django_workflow.Transition', null=True)),
     migrations.AddField(model_name=b'condition', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'callbackparameter', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AddField(model_name=b'callback', name=b'transition', field=models.ForeignKey(verbose_name=b'Transition', to=b'django_workflow.Transition')),
     migrations.AddField(model_name=b'callback', name=b'workflow', field=models.ForeignKey(editable=False, to=b'django_workflow.Workflow', verbose_name=b'Workflow')),
     migrations.AlterUniqueTogether(name=b'transition', unique_together=set([('name', 'initial_state', 'final_state')])),
     migrations.AlterUniqueTogether(name=b'state', unique_together=set([('name', 'workflow')]))]