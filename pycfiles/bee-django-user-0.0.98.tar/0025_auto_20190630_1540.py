# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0025_auto_20190630_1540.py
# Compiled at: 2019-06-30 03:40:39
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0024_userparentrelation')]
    operations = [
     migrations.RenameModel(old_name=b'UserParentRelation', new_name=b'UserProfileParentRelation'),
     migrations.AddField(model_name=b'userprofile', name=b'parents', field=models.ManyToManyField(through=b'bee_django_user.UserProfileParentRelation', to=b'bee_django_user.UserProfile')),
     migrations.AlterField(model_name=b'userprofileparentrelation', name=b'parent', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'parent', to=b'bee_django_user.UserProfile', verbose_name=b'家长')),
     migrations.AlterField(model_name=b'userprofileparentrelation', name=b'student', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'student', to=b'bee_django_user.UserProfile', verbose_name=b'学生'))]