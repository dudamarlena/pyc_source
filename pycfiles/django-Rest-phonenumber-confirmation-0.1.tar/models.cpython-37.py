# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/models.py
# Compiled at: 2020-04-03 12:48:23
# Size of source mod 2**32: 4891 bytes
from random import randint
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.contrib.auth import get_user_model
import django.utils.translation as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_confirmation import app_settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from phonenumber_confirmation.managers import PhoneNumberManager
UserModel = get_user_model()

class PhoneNumber(models.Model):
    user = models.ForeignKey(UserModel, on_delete=(models.CASCADE),
      related_name='user_phone')
    phone = PhoneNumberField(blank=False, null=False,
      unique=(app_settings.UNIQUE_PHONE_NUMBER))
    created = models.DateTimeField(verbose_name=(_('created')), auto_now_add=True)
    verified = models.BooleanField(verbose_name=(_('verified')), default=False)
    primary = models.BooleanField(verbose_name=(_('primary')), default=False)
    objects = PhoneNumberManager()

    class Meta:
        verbose_name = _('phone number ')
        verbose_name_plural = _('Phone Numbers')

    def __str__(self):
        return '%s (%s)' % (self.phone, self.user)

    def send(self, phone_number, confirm):
        pin = randint(100000, 999999)
        if confirm:
            confirmation = PhoneNumberConfirmation.objects.get_or_create(phone_number=phone_number,
              pin=pin).send_confirmation()
        return confirm


class PhoneNumberConfirmation(models.Model):
    phone_number = models.ForeignKey(PhoneNumber, on_delete=(models.CASCADE),
      related_name='phone_number')
    pin = models.IntegerField(verbose_name=(_('pin')), validators=[
     MaxLengthValidator(6)],
      unique=True)
    sent = models.DateTimeField(verbose_name=(_('sent')), null=True)

    class Meta:
        verbose_name = _('phone number confirmation')
        verbose_name_plural = _('Phone Number Confirmations')

    def __str__(self):
        return '%s (%s)' % (self.phone_number, self.pin)

    @classmethod
    def create(cls, phone_number):
        pin = randint(100000, 999999)
        return cls._default_manager.create(phone_number=phone_number, pin=pin)

    def pin_expired(self):
        expiration_date = self.sent + datetime.timedelta(minutes=(app_settings.PHONE_CONFIRMATION_EXPIRE_MINUTES))
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        if all([
         settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN,
         settings.TWILIO_FROM_NUMBER]):
            try:
                twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                twilio_client.messages.create(body=('Your activation pin is %s' % self.pin),
                  to=(str(self.phone_number.phone)),
                  from_=(settings.TWILIO_FROM_NUMBER))
                self.sent = timezone.now()
                self.save()
            except TwilioRestException as e:
                try:
                    raise ValueError(e)
                finally:
                    e = None
                    del e

        else:
            raise ValueError(_('Twilio credentials are not set'))

    def resend_confirmation(self):
        if self.phone_number:
            new_pin = self.pin_expired() or self.phone_number.verified or randint(100000, 999999)
            self.pin = new_pin
            self.save()
        return self.pin

    def confirmation(self, pin):
        if self.pin and self.pin == pin and self.phone_number:
            self.phone_number.verified, self.phone_number.primary = self.pin_expired() or self.phone_number.verified or (True,
                                                                                                                         True)
            self.phone_number.save()
        else:
            raise ValueError('your Pin is wrong or expired, or this phone is verified before.')
        return self.phone_number.verified