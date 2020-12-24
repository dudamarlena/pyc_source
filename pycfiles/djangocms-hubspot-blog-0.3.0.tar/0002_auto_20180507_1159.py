# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmuth/PycharmProjects/djangocms-demo/demo/../github-plugins/djangocms-hubspot-blog/djangocms_hubspot_blog/migrations/0002_auto_20180507_1159.py
# Compiled at: 2018-05-07 05:59:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_hubspot_blog', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'hubspotblogpost', name=b'topics', field=models.ManyToManyField(to=b'djangocms_hubspot_blog.HubspotBlogTopic', verbose_name=b'Topics', blank=True))]