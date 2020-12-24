# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rerb/src/aashe/django-membersuite-auth/django_membersuite_auth/models.py
# Compiled at: 2019-01-16 12:27:58
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from future.utils import python_2_unicode_compatible

@python_2_unicode_compatible
class MemberSuitePortalUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membersuite_id = models.CharField(max_length=64, unique=True)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return (b'<MemberSuitePortalUser: membersuite ID: {membersuite_id}, user ID: {user_id}, is member: {is_member}').format(membersuite_id=self.membersuite_id, user_id=self.user.id, is_member=self.is_member)