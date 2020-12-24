# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/migrations/0001_initial.py
# Compiled at: 2018-03-14 17:20:07
# Size of source mod 2**32: 1070 bytes
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='UMProfile',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'night_mode', models.BooleanField(default=False)),
      (
       'items_per_page', models.PositiveSmallIntegerField(default=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
      (
       'deletion_pending', models.BooleanField(default=False)),
      (
       'user', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), related_name='um_profile', to=(settings.AUTH_USER_MODEL)))])]