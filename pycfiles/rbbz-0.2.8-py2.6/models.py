# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/models.py
# Compiled at: 2014-10-30 01:23:05
import re
from django.contrib.auth.models import User
from django.db import models
from reviewboard.accounts.models import Profile
BZ_IRCNICK_RE = re.compile(':([A-Za-z0-9_\\-\\.]+)')

class BugzillaUserMap(models.Model):
    user = models.OneToOneField(User)
    bugzilla_user_id = models.IntegerField(unique=True, db_index=True)


def placeholder_username(email, bz_user_id):
    return '%s+%s' % (email.split('@')[0], bz_user_id)


def get_or_create_bugzilla_users(user_data):
    users = []
    for user in user_data['users']:
        bz_user_id = user['id']
        email = user['email']
        real_name = user['real_name']
        can_login = user['can_login']
        ircnick_match = BZ_IRCNICK_RE.search(real_name)
        if ircnick_match:
            username = ircnick_match.group(1)
        else:
            username = placeholder_username(email, bz_user_id)
        try:
            bugzilla_user_map = BugzillaUserMap.objects.get(bugzilla_user_id=bz_user_id)
        except BugzillaUserMap.DoesNotExist:
            user = User(username=username, password='!', first_name=real_name, email=email, is_active=can_login)
            try:
                user.save()
            except:
                user.username = placeholder_username(email, bz_user_id)
                user.save()
            else:
                bugzilla_user_map = BugzillaUserMap(user=user, bugzilla_user_id=bz_user_id)
                bugzilla_user_map.save()
        else:
            modified = False
            user = bugzilla_user_map.user
            if user.username != username:
                user.username = username
                modified = True
            if user.email != email:
                user.email = email
                modified = True
            if user.first_name != real_name:
                user.first_name = real_name
                modified = True
            if user.is_active != can_login:
                user.is_active = can_login
                modified = True
            profile = Profile.objects.get_or_create(user=user)[0]
            if not profile.is_private:
                profile.is_private = True
                profile.save()
            if modified:
                try:
                    user.save()
                except:
                    user.username = placeholder_username(email, bz_user_id)
                    user.save()

        users.append(user)

    return users