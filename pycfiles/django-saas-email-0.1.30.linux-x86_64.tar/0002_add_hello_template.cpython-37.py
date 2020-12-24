# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/migrations/0002_add_hello_template.py
# Compiled at: 2018-10-24 06:32:38
# Size of source mod 2**32: 3298 bytes
from __future__ import unicode_literals
from django.db import migrations

def forwards_func(apps, schema_editor):
    MailTemplate = apps.get_model('django_saas_email', 'MailTemplate')
    db_alias = schema_editor.connection.alias
    html_template = '\n    <meta itemprop="name" content="Confirm Email"\n      style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"/>\n<table width="100%" cellpadding="0" cellspacing="0"\n       style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">\n  <tr\n    style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">\n    <td class="content-block"\n        style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"\n        valign="top">\n      <strong>Hello {{first_name}} {{last_name}}!</strong>\n    </td>\n  </tr>\n  <tr\n    style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">\n    <td class="content-block"\n        style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"\n        valign="top">\n      Welcome to django-saas-email :) You can change the template in the MailTemplate admin.\n    </td>\n  </tr>\n  <tr\n    style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">\n    <td class="content-block" itemprop="handler" itemscope itemtype="http://schema.org/HttpActionHandler"\n        style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"\n        valign="top">\n      <a href="http://www.google.com" class="btn-primary" itemprop="url"\n         style="font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #348eda; margin: 0; border-color: #348eda; border-style: solid; border-width: 10px 20px;">Go\n        to google.com</a>\n    </td>\n  </tr>\n</table>\n    '
    MailTemplate.objects.using(db_alias).bulk_create([
     MailTemplate(name='hello', html_template=html_template, subject='Hello {{first_name}} {{last_name}}!')])


def reverse_func(apps, schema_editor):
    MailTemplate = apps.get_model('django_saas_email', 'MailTemplate')
    db_alias = schema_editor.connection.alias
    MailTemplate.objects.using(db_alias).filter(name='hello').delete()


class Migration(migrations.Migration):
    dependencies = [
     ('django_saas_email', '0001_initial')]
    operations = [
     migrations.RunPython(forwards_func, reverse_func)]