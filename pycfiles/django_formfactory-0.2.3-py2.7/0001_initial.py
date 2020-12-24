# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0001_initial.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Action', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'action', models.CharField(choices=[('formfactory.tests.actions.dummy_action', 'formfactory.tests.actions.dummy_action'), ('formfactory.actions.login', 'formfactory.actions.login'), ('formfactory.tests.actions.dummy_wizard_action', 'formfactory.tests.actions.dummy_wizard_action'), ('formfactory.actions.send_email', 'formfactory.actions.send_email'), ('formfactory.actions.store_data', 'formfactory.actions.store_data')], max_length=128))]),
     migrations.CreateModel(name=b'ActionParam', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'key', models.CharField(max_length=128)),
      (
       b'value', models.CharField(max_length=128)),
      (
       b'action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'params', to=b'formfactory.Action'))]),
     migrations.CreateModel(name=b'FieldChoice', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'label', models.CharField(max_length=128)),
      (
       b'value', models.CharField(max_length=128))], options={b'ordering': [
                    b'label']}),
     migrations.CreateModel(name=b'FieldGroupFormThrough', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order', models.PositiveIntegerField(default=0))], options={b'ordering': [
                    b'order'], 
        b'verbose_name': b'Field Group', 
        b'verbose_name_plural': b'Field Groups'}),
     migrations.CreateModel(name=b'FieldGroupThrough', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order', models.PositiveIntegerField(default=0))], options={b'ordering': [
                    b'order'], 
        b'verbose_name': b'Field', 
        b'verbose_name_plural': b'Fields'}),
     migrations.CreateModel(name=b'Form', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256, unique=True)),
      (
       b'success_message', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'failure_message', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'post_to', models.CharField(blank=True, help_text=b'URL to which this form will be posted to. Leave blank to                     post back to original view.', max_length=256, null=True)),
      (
       b'redirect_to', models.CharField(blank=True, help_text=b'URL to which this form will redirect to after processesing.', max_length=256, null=True)),
      (
       b'submit_button_text', models.CharField(default=b'Submit', help_text=b'The text you would like on the form submit button.', max_length=64))], options={b'ordering': [
                    b'title']}),
     migrations.CreateModel(name=b'FormActionThrough', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order', models.PositiveIntegerField(default=0)),
      (
       b'action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Action')),
      (
       b'form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Form'))], options={b'ordering': [
                    b'order'], 
        b'verbose_name': b'Form Action', 
        b'verbose_name_plural': b'Form Actions'}),
     migrations.CreateModel(name=b'FormData', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'uuid', models.UUIDField(db_index=True)),
      (
       b'form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Form'))], options={b'ordering': [
                    b'uuid']}),
     migrations.CreateModel(name=b'FormDataItem', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'value', models.TextField()),
      (
       b'form_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'items', to=b'formfactory.FormData'))]),
     migrations.CreateModel(name=b'FormField', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256, unique=True)),
      (
       b'field_type', models.CharField(choices=[('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('ChoiceField', 'ChoiceField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FloatField', 'FloatField'), ('GenericIPAddressField', 'GenericIPAddressField'), ('IntegerField', 'IntegerField'), ('MultipleChoiceField', 'MultipleChoiceField'), ('SlugField', 'SlugField'), ('SplitDateTimeField', 'SplitDateTimeField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('UUIDField', 'UUIDField')], max_length=128)),
      (
       b'widget', models.CharField(blank=True, choices=[('TextInput', 'TextInput'), ('NumberInput', 'NumberInput'), ('EmailInput', 'EmailInput'), ('URLInput', 'URLInput'), ('PasswordInput', 'PasswordInput'), ('HiddenInput', 'HiddenInput'), ('DateInput', 'DateInput'), ('DateTimeInput', 'DateTimeInput'), ('TimeInput', 'TimeInput'), ('Textarea', 'Textarea'), ('CheckboxInput', 'CheckboxInput'), ('Select', 'Select'), ('NullBooleanSelect', 'NullBooleanSelect'), ('SelectMultiple', 'SelectMultiple'), ('RadioSelect', 'RadioSelect'), ('CheckboxSelectMultiple', 'CheckboxSelectMultiple')], help_text=b'Leave blank if you prefer to use the default widget.', max_length=128, null=True)),
      (
       b'label', models.CharField(blank=True, max_length=64, null=True)),
      (
       b'initial', models.TextField(blank=True, null=True)),
      (
       b'max_length', models.PositiveIntegerField(blank=True, default=256, null=True)),
      (
       b'help_text', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'placeholder', models.CharField(blank=True, max_length=128, null=True)),
      (
       b'required', models.BooleanField(default=True)),
      (
       b'disabled', models.BooleanField(default=False)),
      (
       b'additional_validators', models.CharField(blank=True, choices=[('formfactory.tests.validators.dummy_validator', 'formfactory.tests.validators.dummy_validator')], max_length=128, null=True)),
      (
       b'choices', models.ManyToManyField(blank=True, null=True, to=b'formfactory.FieldChoice'))]),
     migrations.CreateModel(name=b'FormFieldGroup', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'forms', models.ManyToManyField(related_name=b'fieldgroups', through=b'formfactory.FieldGroupFormThrough', to=b'formfactory.Form'))]),
     migrations.CreateModel(name=b'Wizard', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256, unique=True)),
      (
       b'success_message', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'failure_message', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'post_to', models.CharField(blank=True, help_text=b'URL to which this form will be posted to. Leave blank to                     post back to original view.', max_length=256, null=True)),
      (
       b'redirect_to', models.CharField(blank=True, help_text=b'URL to which this form will redirect to after processesing.', max_length=256, null=True)),
      (
       b'submit_button_text', models.CharField(default=b'Submit', help_text=b'The text you would like on the form submit button.', max_length=64))], options={b'abstract': False}),
     migrations.CreateModel(name=b'WizardActionThrough', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order', models.PositiveIntegerField(default=0)),
      (
       b'action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Action')),
      (
       b'wizard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Wizard'))], options={b'ordering': [
                    b'order'], 
        b'verbose_name': b'Wizard Action', 
        b'verbose_name_plural': b'Wizard Actions'}),
     migrations.CreateModel(name=b'WizardFormThrough', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order', models.PositiveIntegerField(default=0)),
      (
       b'form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Form')),
      (
       b'wizard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Wizard'))], options={b'ordering': [
                    b'order'], 
        b'verbose_name': b'Form', 
        b'verbose_name_plural': b'Forms'}),
     migrations.AddField(model_name=b'wizard', name=b'actions', field=models.ManyToManyField(through=b'formfactory.WizardActionThrough', to=b'formfactory.Action')),
     migrations.AddField(model_name=b'wizard', name=b'forms', field=models.ManyToManyField(through=b'formfactory.WizardFormThrough', to=b'formfactory.Form')),
     migrations.AddField(model_name=b'formfield', name=b'field_groups', field=models.ManyToManyField(related_name=b'fields', through=b'formfactory.FieldGroupThrough', to=b'formfactory.FormFieldGroup')),
     migrations.AddField(model_name=b'formdataitem', name=b'form_field', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.FormField')),
     migrations.AddField(model_name=b'form', name=b'actions', field=models.ManyToManyField(through=b'formfactory.FormActionThrough', to=b'formfactory.Action')),
     migrations.AddField(model_name=b'fieldgroupthrough', name=b'field', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.FormField')),
     migrations.AddField(model_name=b'fieldgroupthrough', name=b'field_group', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.FormFieldGroup')),
     migrations.AddField(model_name=b'fieldgroupformthrough', name=b'field_group', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.FormFieldGroup')),
     migrations.AddField(model_name=b'fieldgroupformthrough', name=b'form', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.Form'))]