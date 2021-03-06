# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/contrib/tracker/migrations/0001_initial.py
# Compiled at: 2018-08-25 11:08:59
# Size of source mod 2**32: 2431 bytes
from django.conf import settings
import workon
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='TrackEvent',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'timestamp', models.FloatField(verbose_name='TS')),
      (
       'tracked_at', models.DateTimeField(verbose_name='Tracké à')),
      (
       'action', models.CharField(max_length=254, verbose_name='Action')),
      (
       'object_id', models.PositiveIntegerField(editable=False, null=True)),
      (
       'object_repr', models.CharField(editable=False, max_length=250, verbose_name='Object representation')),
      (
       'field_name', models.CharField(max_length=254, verbose_name='Field')),
      (
       'old_value', models.TextField(editable=False, null=True, verbose_name='Old value')),
      (
       'new_value', models.TextField(editable=False, null=True, verbose_name='New value')),
      (
       'm2m_pk_set', workon.ArrayField(base_field=models.PositiveIntegerField(verbose_name='pk'), null=True, size=None)),
      (
       'm2m_repr_set', workon.ArrayField(base_field=models.CharField(max_length=254, verbose_name='Repr'), null=True, size=None)),
      (
       'user_repr', models.CharField(blank=True, help_text='User representation, useful if the user is deleted later.', max_length=250, null=True, verbose_name='User representation')),
      (
       'object_content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='track_object_content_type', to='contenttypes.ContentType')),
      (
       'user', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), verbose_name='Executé par'))],
       options={'verbose_name':'Model Tracking event', 
      'verbose_name_plural':'Model Tracking events', 
      'ordering':[
       '-tracked_at']})]