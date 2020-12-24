# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/notification/migrations/0003_tempemailnotification.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1799 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def populate_temp_emails(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    EmailNotification = apps.get_model('notification', 'EmailNotification')
    TempEmailNotification = apps.get_model('notification', 'TempEmailNotification')
    for email in EmailNotification.objects.using(db_alias):
        temp_email = TempEmailNotification.objects.using(db_alias).create(name=(email.name),
          subject=(email.subject),
          body=(email.body))
        for site in email.sites.all():
            temp_email.sites.add(site.id)


def delete_temp_emails(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    TempEmailNotification = apps.get_model('notification', 'TempEmailNotification')
    TempEmailNotification.objects.using(db_alias).delete()


class Migration(migrations.Migration):
    dependencies = [
     ('notification', '0002_emailnotification_sites')]
    operations = [
     migrations.CreateModel(name='TempEmailNotification',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'name', models.CharField(max_length=50)),
      (
       'subject', models.CharField(max_length=77)),
      (
       'body', models.TextField()),
      (
       'sites', models.ManyToManyField(to='sites.Site'))]),
     migrations.RunPython(populate_temp_emails, delete_temp_emails)]