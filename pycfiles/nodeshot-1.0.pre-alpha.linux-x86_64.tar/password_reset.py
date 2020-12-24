# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/profiles/models/password_reset.py
# Compiled at: 2014-09-07 09:35:39
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.http import int_to_base36
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator as token_generator
from nodeshot.core.base.utils import now
from ..settings import settings

class PasswordResetManager(models.Manager):
    """ Password Reset Manager """

    def create_for_user(self, user):
        """ create password reset for specified user """
        if type(user) is unicode:
            from .profile import Profile as User
            user = User.objects.get(email=user)
        temp_key = token_generator.make_token(user)
        password_reset = PasswordReset(user=user, temp_key=temp_key)
        password_reset.save()
        subject = _('Password reset email sent')
        message = render_to_string('profiles/email_messages/password_reset_key_message.txt', {'user': user, 
           'uid': int_to_base36(user.id), 
           'temp_key': temp_key, 
           'site_url': settings.SITE_URL, 
           'site_name': settings.SITE_NAME})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return password_reset


class PasswordReset(models.Model):
    """
    Password reset Key
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    temp_key = models.CharField(_('temp_key'), max_length=100)
    timestamp = models.DateTimeField(_('timestamp'), default=now)
    reset = models.BooleanField(_('reset yet?'), default=False)
    objects = PasswordResetManager()

    class Meta:
        verbose_name = _('password reset')
        verbose_name_plural = _('password resets')
        app_label = 'profiles'

    def __unicode__(self):
        return '%s (key=%s, reset=%r)' % (
         self.user.username,
         self.temp_key,
         self.reset)