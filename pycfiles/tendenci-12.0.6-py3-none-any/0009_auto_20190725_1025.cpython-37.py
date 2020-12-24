# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0009_auto_20190725_1025.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1103 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0008_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='membershipappfield',
       name='field_type',
       field=models.CharField(blank=True, choices=[('', 'Set to Default'), ('CharField', 'Text'), ('CharField/django.forms.Textarea', 'Paragraph Text'), ('BooleanField', 'Checkbox'), ('ChoiceField', 'Select One (Drop Down)'), ('ChoiceField/django.forms.RadioSelect', 'Select One (Radio Buttons)'), ('MultipleChoiceField', 'Multi select (Drop Down)'), ('MultipleChoiceField/django.forms.CheckboxSelectMultiple', 'Multi select (Checkboxes)'), ('CountrySelectField', 'Countries Drop Down'), ('EmailField', 'Email'), ('FileField', 'File upload'), ('DateField/django.forms.widgets.SelectDateWidget', 'Date'), ('DateTimeField', 'Date/time'), ('section_break', 'Section Break')], max_length=64, verbose_name='Field Type'))]