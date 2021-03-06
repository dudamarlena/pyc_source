# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0001_initial.py
# Compiled at: 2016-08-31 15:02:52
# Size of source mod 2**32: 4800 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, dyn_struct.db.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='DynamicStructure',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=255, unique=True, verbose_name='Название'))],
       options={'verbose_name':'динамическая структура', 
      'verbose_name_plural':'динамические структуры'}),
     migrations.CreateModel(name='DynamicStructureField',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'header', models.CharField(blank=True, help_text='при заполнении этого поля, вместо поля формы будет выводить заголовок', max_length=255, verbose_name='заголовок')),
      (
       'name', models.CharField(blank=True, max_length=255, unique=True, verbose_name='Название')),
      (
       'form_field', models.CharField(blank=True, choices=[('Field', 'Field'), ('CharField', 'CharField'), ('IntegerField', 'IntegerField'), ('DateField', 'DateField'), ('TimeField', 'TimeField'), ('DateTimeField', 'DateTimeField'), ('DurationField', 'DurationField'), ('RegexField', 'RegexField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('ImageField', 'ImageField'), ('URLField', 'URLField'), ('BooleanField', 'BooleanField'), ('NullBooleanField', 'NullBooleanField'), ('ChoiceField', 'ChoiceField'), ('MultipleChoiceField', 'MultipleChoiceField'), ('ComboField', 'ComboField'), ('MultiValueField', 'MultiValueField'), ('FloatField', 'FloatField'), ('DecimalField', 'DecimalField'), ('SplitDateTimeField', 'SplitDateTimeField'), ('GenericIPAddressField', 'GenericIPAddressField'), ('FilePathField', 'FilePathField'), ('SlugField', 'SlugField'), ('TypedChoiceField', 'TypedChoiceField'), ('TypedMultipleChoiceField', 'TypedMultipleChoiceField'), ('UUIDField', 'UUIDField')], max_length=255, verbose_name='Поле')),
      (
       'form_kwargs', dyn_struct.db.fields.ParamsField(default='{}', help_text='{"key": value, ... }  / Используйте только двойные кавычки ( " )', verbose_name='Параметры поля')),
      (
       'widget', models.CharField(blank=True, choices=[('Media', 'Media'), ('MediaDefiningClass', 'MediaDefiningClass'), ('Widget', 'Widget'), ('TextInput', 'TextInput'), ('NumberInput', 'NumberInput'), ('EmailInput', 'EmailInput'), ('URLInput', 'URLInput'), ('PasswordInput', 'PasswordInput'), ('HiddenInput', 'HiddenInput'), ('MultipleHiddenInput', 'MultipleHiddenInput'), ('FileInput', 'FileInput'), ('ClearableFileInput', 'ClearableFileInput'), ('Textarea', 'Textarea'), ('DateInput', 'DateInput'), ('DateTimeInput', 'DateTimeInput'), ('TimeInput', 'TimeInput'), ('CheckboxInput', 'CheckboxInput'), ('Select', 'Select'), ('NullBooleanSelect', 'NullBooleanSelect'), ('SelectMultiple', 'SelectMultiple'), ('RadioSelect', 'RadioSelect'), ('CheckboxSelectMultiple', 'CheckboxSelectMultiple'), ('MultiWidget', 'MultiWidget'), ('SplitDateTimeWidget', 'SplitDateTimeWidget'), ('SplitHiddenDateTimeWidget', 'SplitHiddenDateTimeWidget'), ('SelectDateWidget', 'SelectDateWidget')], max_length=255, verbose_name='Виджет')),
      (
       'widget_kwargs', dyn_struct.db.fields.ParamsField(default='{}', help_text='{"key": value, ... }  / Используйте только двойные кавычки ( " )', verbose_name='Параметры виджета')),
      (
       'row', models.PositiveSmallIntegerField(verbose_name='Строка')),
      (
       'position', models.PositiveSmallIntegerField(verbose_name='Позиция в строке')),
      (
       'classes', models.CharField(blank=True, help_text='col-md-3, custom-class ...', max_length=255, verbose_name='CSS-классы')),
      (
       'structure', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='fields', to='dyn_struct.DynamicStructure', verbose_name='Динамический объект'))],
       options={'verbose_name':'поле динамической структуры', 
      'verbose_name_plural':'поля динамических структур'})]