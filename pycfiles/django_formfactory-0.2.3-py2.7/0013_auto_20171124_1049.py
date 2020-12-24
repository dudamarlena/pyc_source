# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0013_auto_20171124_1049.py
# Compiled at: 2017-11-28 02:59:59
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0012_auto_20170703_1030')]
    operations = [
     migrations.AlterField(model_name=b'action', name=b'action', field=models.CharField(choices=[('formfactory.actions.file_upload', 'formfactory.actions.file_upload'), ('formfactory.actions.login', 'formfactory.actions.login'), ('formfactory.actions.send_email', 'formfactory.actions.send_email'), ('formfactory.actions.store_data', 'formfactory.actions.store_data')], max_length=128)),
     migrations.AlterField(model_name=b'customerrormessage', name=b'key', field=models.CharField(choices=[('empty', 'empty'), ('incomplete', 'incomplete'), ('invalid', 'invalid'), ('invalid_choice', 'invalid_choice'), ('invalid_image', 'invalid_image'), ('invalid_list', 'invalid_list'), ('invalid_date', 'invalid_date'), ('invalid_time', 'invalid_time'), ('invalid_pk_value', 'invalid_pk_value'), ('list', 'list'), ('max_decimal_places', 'max_decimal_places'), ('max_digits', 'max_digits'), ('max_length', 'max_length'), ('max_value', 'max_value'), ('max_whole_digits', 'max_whole_digits'), ('min_length', 'min_length'), ('min_value', 'min_value'), ('missing', 'missing'), ('required', 'required')], max_length=128)),
     migrations.AlterField(model_name=b'formfield', name=b'choices', field=models.ManyToManyField(blank=True, to=b'formfactory.FieldChoice')),
     migrations.AlterField(model_name=b'formfield', name=b'field_type', field=models.CharField(choices=[('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('ChoiceField', 'ChoiceField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('FloatField', 'FloatField'), ('GenericIPAddressField', 'GenericIPAddressField'), ('IntegerField', 'IntegerField'), ('MultipleChoiceField', 'MultipleChoiceField'), ('SlugField', 'SlugField'), ('SplitDateTimeField', 'SplitDateTimeField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('UUIDField', 'UUIDField')], max_length=128)),
     migrations.AlterField(model_name=b'formfield', name=b'widget', field=models.CharField(blank=True, choices=[('CheckboxInput', 'CheckboxInput'), ('CheckboxSelectMultiple', 'CheckboxSelectMultiple'), ('DateInput', 'DateInput'), ('DateTimeInput', 'DateTimeInput'), ('EmailInput', 'EmailInput'), ('FileInput', 'FileInput'), ('HiddenInput', 'HiddenInput'), ('NullBooleanSelect', 'NullBooleanSelect'), ('NumberInput', 'NumberInput'), ('PasswordInput', 'PasswordInput'), ('RadioSelect', 'RadioSelect'), ('Select', 'Select'), ('SelectMultiple', 'SelectMultiple'), ('Textarea', 'Textarea'), ('TextInput', 'TextInput'), ('TimeInput', 'TimeInput'), ('URLInput', 'URLInput')], help_text=b'Leave blank if you prefer to use the default widget.', max_length=128, null=True))]