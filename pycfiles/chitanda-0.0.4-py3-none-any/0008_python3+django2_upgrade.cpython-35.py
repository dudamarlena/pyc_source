# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0008_python3+django2_upgrade.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 1824 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0007_registration_grading_started')]
    operations = [
     migrations.AlterField(model_name='course', name='extension_policy', field=models.CharField(choices=[('per-team', 'Extensions per team'), ('per-student', 'Extensions per student')], default='per-student', max_length=16)),
     migrations.AlterField(model_name='course', name='git_staging_usernames', field=models.CharField(choices=[('user-id', 'Same as user id'), ('custom', 'Custom git username')], default='user-id', max_length=16)),
     migrations.AlterField(model_name='course', name='git_usernames', field=models.CharField(choices=[('user-id', 'Same as user id'), ('custom', 'Custom git username')], default='user-id', max_length=16)),
     migrations.AlterField(model_name='registration', name='final_submission', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='final_submission_of', to='api.Submission')),
     migrations.AlterField(model_name='registration', name='grader', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Grader')),
     migrations.AlterField(model_name='submission', name='submitted_by', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))]