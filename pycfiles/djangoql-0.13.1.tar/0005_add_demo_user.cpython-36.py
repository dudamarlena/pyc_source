# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0005_add_demo_user.py
# Compiled at: 2019-02-20 11:36:53
# Size of source mod 2**32: 511 bytes
from django.db import migrations
from django.conf import settings
from django.contrib.auth.hashers import make_password

def create_demo_user(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    User.objects.create(username='demo',
      password=(make_password('demo')))


class Migration(migrations.Migration):
    dependencies = [
     ('core', '0004_book_similar_books_related_name')]
    operations = [
     migrations.RunPython(create_demo_user)]