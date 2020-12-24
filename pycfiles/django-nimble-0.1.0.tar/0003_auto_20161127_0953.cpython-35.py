# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\migrations\0003_auto_20161127_0953.py
# Compiled at: 2016-12-18 13:13:20
# Size of source mod 2**32: 2527 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('nimble', '0002_profile_theme')]
    operations = [
     migrations.CreateModel(name='Story', fields=[
      (
       'id',
       models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=30))], options={'abstract': False}),
     migrations.CreateModel(name='Debt', fields=[
      (
       'story_ptr',
       models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='nimble.Story'))], options={'abstract': False}, bases=('nimble.story', )),
     migrations.CreateModel(name='Feature', fields=[
      (
       'story_ptr',
       models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='nimble.Story'))], options={'abstract': False}, bases=('nimble.story', )),
     migrations.AddField(model_name='story', name='author', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
     migrations.AddField(model_name='story', name='polymorphic_ctype', field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_nimble.story_set+', to='contenttypes.ContentType'))]