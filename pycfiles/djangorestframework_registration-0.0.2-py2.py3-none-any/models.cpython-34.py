# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eugene/Workspace/django-rest-framework-registration/rest_framework_registration/models.py
# Compiled at: 2016-03-31 12:24:12
# Size of source mod 2**32: 1571 bytes
from django.db import models
from django.utils.crypto import get_random_string
User = get_user_model()

class RegistrationProfileManager(models.Manager):

    def activate_profile(self, activation_key):
        try:
            profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False

        if not profile.activation_key_expired():
            user = profile.user
            user.is_active = True
            user.save()
            profile.activation_key = self.model.ACTIVATED
            profile.save()
            return user
        return False

    def create_profile(self, user):
        activation_key = hashlib.sha1(get_random_string(12)).digest()
        self.create(user=user, activation_key=activation_key)


class RegistrationProfile(models.Model):
    ACTIVATED = 'ALREADY_ACTIVATED'
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=40)
    objects = RegistrationProfileManager()

    def is_activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or self.user.date_joined + expiration_date <= timezone.now()

    def send_activation_email(self):
        ctx = {'activation_key': self.activation_key}
        message = render_to_string('registration/activation_email.txt', ctx)
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)