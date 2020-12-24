# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-users/ovp_users/models/profile.py
# Compiled at: 2017-02-24 13:31:00
# Size of source mod 2**32: 784 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ovp_users.helpers import get_settings, import_from_string

class UserProfile(models.Model):
    user = models.OneToOneField('User', blank=True, null=True, related_name='%(app_label)s_%(class)s_profile')
    full_name = models.CharField(_('Full name'), max_length=300, null=True, blank=True)
    skills = models.ManyToManyField('ovp_core.Skill')
    causes = models.ManyToManyField('ovp_core.Cause')
    about = models.TextField(_('About me'), null=True, blank=True)
    public = models.BooleanField(_('Public Profile'), default=True)


def get_profile_model():
    s = get_settings()
    class_path = s.get('PROFILE_MODEL', None)
    if class_path:
        return import_from_string(class_path)
    return UserProfile