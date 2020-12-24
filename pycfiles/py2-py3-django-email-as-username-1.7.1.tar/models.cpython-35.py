# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/models.py
# Compiled at: 2015-10-23 08:44:12
# Size of source mod 2**32: 1929 bytes
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from emailusernames.forms import EmailAdminAuthenticationForm
from emailusernames.utils import _email_to_username

def user_init_patch(self, *args, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    self._username = self.username
    if self.username == _email_to_username(self.email):
        self.username = self.email


def user_save_patch(self, *args, **kwargs):
    email_as_username = self.username.lower() == self.email.lower()
    if self.pk is not None:
        try:
            old_user = self.__class__.objects.get(pk=self.pk)
            email_as_username = email_as_username or '@' in self.username and old_user.username == old_user.email
        except self.__class__.DoesNotExist:
            pass

    if email_as_username:
        self.username = _email_to_username(self.email)
    try:
        super(User, self).save_base(*args, **kwargs)
    finally:
        if email_as_username:
            self.username = self.email


original_init = User.__init__
original_save_base = User.save_base

def monkeypatch_user():
    User.__init__ = user_init_patch
    User.save_base = user_save_patch


def unmonkeypatch_user():
    User.__init__ = original_init
    User.save_base = original_save_base


monkeypatch_user()
AdminSite.login_form = EmailAdminAuthenticationForm
AdminSite.login_template = 'email_usernames/login.html'