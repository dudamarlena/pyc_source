# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/contactus/migrations/0003_auto_20181126_1132.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 631 bytes
from django.db import migrations

def remove_all_records(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Object = apps.get_model('contactus', 'ContactUs')
    Object.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
     ('contactus', '0002_auto_20181125_2227')]
    operations = [
     migrations.RunPython(remove_all_records, reverse_code=(migrations.RunPython.noop))]