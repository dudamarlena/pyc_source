# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0001_initial.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 12738 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.db import migrations, models
import callisto_core.wizard_builder.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='Choice',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'text', models.TextField()),
      (
       'position',
       models.PositiveSmallIntegerField(default=0,
         verbose_name='Position')),
      (
       'extra_info_placeholder',
       models.CharField(blank=True,
         max_length=500,
         verbose_name='Placeholder for extra info field (leave blank for no field)'))],
       options={'ordering': ['position', 'pk']}),
     migrations.CreateModel(name='Conditional',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'condition_type',
       models.CharField(choices=[
        ('and', 'exactly'), ('or', 'in')],
         default='and',
         max_length=50)),
      (
       'answer', models.CharField(max_length=150))]),
     migrations.CreateModel(name='FormQuestion',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'text', models.TextField()),
      (
       'position',
       models.PositiveSmallIntegerField(default=0,
         verbose_name='position')),
      (
       'example', models.TextField(blank=True)),
      (
       'descriptive_text', models.TextField(blank=True)),
      (
       'added', models.DateTimeField(auto_now_add=True))],
       options={'verbose_name':'question', 
      'ordering':['position']}),
     migrations.CreateModel(name='PageBase',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'position',
       models.PositiveSmallIntegerField(default=0,
         verbose_name='position')),
      (
       'section',
       models.IntegerField(choices=[
        (1, 'When'), (2, 'Where'), (3, 'What'), (4, 'Who')],
         default=1))],
       options={'verbose_name':'Form page', 
      'ordering':['position']}),
     migrations.CreateModel(name='Date',
       fields=[
      (
       'formquestion_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.FormQuestion'))],
       options={'abstract': False},
       bases=('wizard_builder.formquestion', )),
     migrations.CreateModel(name='MultiLineText',
       fields=[
      (
       'formquestion_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.FormQuestion'))],
       options={'abstract': False},
       bases=('wizard_builder.formquestion', )),
     migrations.CreateModel(name='MultipleChoice',
       fields=[
      (
       'formquestion_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.FormQuestion'))],
       options={'abstract': False},
       bases=('wizard_builder.formquestion', )),
     migrations.CreateModel(name='QuestionPage',
       fields=[
      (
       'pagebase_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.PageBase')),
      (
       'encouragement', models.TextField(blank=True)),
      (
       'infobox',
       models.TextField(blank=True,
         verbose_name='why is this asked? wrap additional titles in [[double brackets]]')),
      (
       'multiple',
       models.BooleanField(default=False,
         verbose_name='User can add multiple')),
      (
       'name_for_multiple',
       models.TextField(blank=True,
         verbose_name='name of field for "add another" prompt'))],
       options={'ordering': ['position']},
       bases=('wizard_builder.pagebase', )),
     migrations.CreateModel(name='SingleLineText',
       fields=[
      (
       'formquestion_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.FormQuestion'))],
       options={'abstract': False},
       bases=('wizard_builder.formquestion', )),
     migrations.CreateModel(name='SingleLineTextWithMap',
       fields=[
      (
       'formquestion_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.FormQuestion')),
      (
       'map_link', models.CharField(max_length=500))],
       options={'abstract': False},
       bases=('wizard_builder.formquestion', )),
     migrations.CreateModel(name='TextPage',
       fields=[
      (
       'pagebase_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.PageBase')),
      (
       'title', models.TextField(blank=True)),
      (
       'text', models.TextField())],
       options={'abstract': False},
       bases=('wizard_builder.pagebase', )),
     migrations.AddField(model_name='pagebase',
       name='polymorphic_ctype',
       field=models.ForeignKey(editable=False,
       null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       related_name='polymorphic_wizard_builder.pagebase_set+',
       to='contenttypes.ContentType')),
     migrations.AddField(model_name='formquestion',
       name='polymorphic_ctype',
       field=models.ForeignKey(editable=False,
       null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       related_name='polymorphic_wizard_builder.formquestion_set+',
       to='contenttypes.ContentType')),
     migrations.AddField(model_name='conditional',
       name='page',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE),
       to='wizard_builder.PageBase')),
     migrations.AddField(model_name='conditional',
       name='question',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       to='wizard_builder.FormQuestion')),
     migrations.CreateModel(name='Checkbox',
       fields=[
      (
       'multiplechoice_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.MultipleChoice'))],
       options={'abstract': False},
       bases=('wizard_builder.multiplechoice', )),
     migrations.CreateModel(name='RadioButton',
       fields=[
      (
       'multiplechoice_ptr',
       models.OneToOneField(auto_created=True,
         on_delete=(django.db.models.deletion.CASCADE),
         parent_link=True,
         primary_key=True,
         serialize=False,
         to='wizard_builder.MultipleChoice')),
      (
       'is_dropdown', models.BooleanField(default=False))],
       options={'abstract': False},
       bases=('wizard_builder.multiplechoice', )),
     migrations.AddField(model_name='formquestion',
       name='page',
       field=models.ForeignKey(null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       to='wizard_builder.QuestionPage')),
     migrations.AddField(model_name='choice',
       name='question',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       to='wizard_builder.MultipleChoice'))]