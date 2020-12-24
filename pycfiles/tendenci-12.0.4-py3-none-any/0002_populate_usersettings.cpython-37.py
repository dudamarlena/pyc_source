# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0002_populate_usersettings.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1404 bytes
from django.contrib.auth import get_user_model
from django.db import migrations
from tendenci.apps.helpdesk.settings import DEFAULT_USER_SETTINGS

def pickle_settings(data):
    """Pickling as defined at migration's creation time"""
    import pickle
    from base64 import b64encode
    return b64encode(pickle.dumps(data)).decode()


def populate_usersettings(apps, schema_editor):
    """Create a UserSettings entry for each existing user.
    This will only happen once (at install time, or at upgrade)
    when the UserSettings model doesn't already exist."""
    _User = get_user_model()
    User = apps.get_model(_User._meta.app_label, _User._meta.model_name)
    UserSettings = apps.get_model('helpdesk', 'UserSettings')
    settings_pickled = pickle_settings(DEFAULT_USER_SETTINGS)
    for u in User.objects.all():
        try:
            UserSettings.objects.get(user=u)
        except UserSettings.DoesNotExist:
            UserSettings.objects.create(user=u, settings_pickled=settings_pickled)


def noop(*args, **kwargs):
    pass


class Migration(migrations.Migration):
    dependencies = [
     ('helpdesk', '0001_initial')]
    operations = [
     migrations.RunPython(populate_usersettings, reverse_code=noop)]