# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/models.py
# Compiled at: 2012-11-19 10:17:49
import json
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

class Service(models.Model):
    """
    Service class represent a web application that use Daarmaan as its
    authentication service.
    """
    name = models.CharField(_('service'), max_length=64, unique=True)
    key = models.CharField(_('key'), max_length=256)
    default_url = models.URLField(_('Default URL'), blank=True, null=True)
    active = models.BooleanField(_('active'), default=False)
    user = models.ForeignKey('auth.User', verbose_name=_('User'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('Services')


class Profile(models.Model):
    """
    User profile model related to each service.
    """
    user = models.ForeignKey('auth.User', verbose_name=_('permissions'))
    service = models.ForeignKey(Service, verbose_name=_('service'))
    _profile_data = models.TextField(_('service profile'))

    @property
    def data(self):
        return json.loads(self._profile_data)

    @data.setter
    def data(self, value):
        self._profile_data = json.dumps(value)
        return json.dumps(value)

    def __unicode__(self):
        return self.user.username

    class Meta:
        unique_together = [
         'user', 'service']
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


class UserServices(models.Model):
    """
    Services that user have access to.
    """
    user = models.ForeignKey('auth.User', verbose_name=_('permissions'))
    services = models.ManyToManyField(Service, verbose_name=_('service'))

    def __unicode__(self):
        return '%s services' % self.user

    class Meta:
        verbose_name = _('user services')
        verbose_name_plural = _('user services')


class VerificationCode(models.Model):
    """
    Verification code model. This model will contain all the
    verification codes that will sent to users.
    """
    user = models.ForeignKey('auth.User', verbose_name=_('permissions'), unique=True)
    code = models.CharField(_('code'), max_length=40, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    DEFAULT_VALID_TIME = 48

    @classmethod
    def cleanup(cls):
        from datetime import timedelta, datetime
        valid_time = getattr(settings, 'VALIDATION_TIME', cls.DEFAULT_VALID_TIME)
        pasted_48 = datetime.now() - timedelta(hours=valid_time)
        cls.objects.filter(timestamp__lt=pasted_48).delete()

    @classmethod
    def generate(cls, user):
        """
        Generate a verification code. At first look for exists
        valid code.
        """
        try:
            code = cls.objects.get(user=user)
            if code.is_valid():
                return code.code
            cls.cleanup()
        except cls.DoesNotExist:
            pass

        import hashlib
        from datetime import datetime
        m = hashlib.sha1()
        m.update('%s%s' % (user.username,
         datetime.now()))
        code = cls(user=user, code=m.hexdigest())
        code.save()
        return code.code

    def _valid_range(self):
        """
        Returns a valid range of time.
        """
        from datetime import timedelta, datetime
        valid_time = getattr(settings, 'VALIDATION_TIME', self.DEFAULT_VALID_TIME)
        return datetime.now() - timedelta(hours=valid_time)

    def is_valid(self):
        """
        Does verification code belongs to a valid time range.
        """
        pasted_48 = self._valid_range()
        timestamp = self.timestamp.replace(tzinfo=None)
        if timestamp < pasted_48:
            return False
        else:
            return True


class BasicProfile(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('permissions'), unique=True)
    public = models.BooleanField(_('public profile'), default=False)

    def is_public(self):
        return self.public

    def __unicode__(self):
        return '%s basic profile' % self.user

    class Meta:
        verbose_name = _('user services')
        verbose_name_plural = _('user services')