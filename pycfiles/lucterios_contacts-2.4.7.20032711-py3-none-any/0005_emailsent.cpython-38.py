# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/mailing/migrations/0005_emailsent.py
# Compiled at: 2020-03-26 06:35:18
# Size of source mod 2**32: 1887 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('contacts', '0004_length_field'),
     ('mailing', '0004_add_documents')]
    operations = [
     migrations.CreateModel(name='EmailSent',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'email', models.CharField(max_length=50, verbose_name='email')),
      (
       'date', models.DateTimeField(null=True, verbose_name='date')),
      (
       'success', models.BooleanField(default=False, verbose_name='success')),
      (
       'error', models.TextField(default='', verbose_name='error')),
      (
       'contact', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='contacts.AbstractContact', verbose_name='contact'))],
       options={'verbose_name':'email sent info', 
      'ordering':[
       '-last_open_date', 'contact', '-date', 'email'], 
      'default_permissions':[],  'verbose_name_plural':'email sent info'}),
     migrations.AlterModelOptions(name='message',
       options={'verbose_name':'message', 
      'verbose_name_plural':'messages',  'ordering':['-date']}),
     migrations.AddField(model_name='message',
       name='email_to_send',
       field=models.TextField(default='', verbose_name='email to send')),
     migrations.AddField(model_name='emailsent',
       name='message',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='mailing.Message', verbose_name='message'))]