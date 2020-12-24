# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0005_auto_20190613_1815.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1043 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    QA = apps.get_model('questionanswers', 'QA')
    for obj in QA.objects.all():
        obj.model_obj2 = obj.model_obj
        obj.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    QA = apps.get_model('questionanswers', 'QA')
    for obj in QA.objects.all():
        obj.model_obj = obj.model_obj2
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
     ('questionanswers', '0004_qa_model_obj2')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]