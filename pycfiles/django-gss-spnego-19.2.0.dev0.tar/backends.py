# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/bewing/PycharmProjects/django-gss-spnego/src/django_gss_spnego/backends.py
# Compiled at: 2019-02-13 14:34:45
import base64, binascii, gssapi, logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
logger = logging.getLogger(__name__)

class SpnegoBackendMixin(object):

    def authenticate(self, request, spnego=None, **kwargs):
        if spnego is None:
            return super(SpnegoBackendMixin, self).authenticate(request, **kwargs)
        else:
            try:
                token = base64.b64decode(spnego)
                credentials = gssapi.creds.Credentials(usage='accept')
                context = gssapi.SecurityContext(creds=credentials)
                response = context.step(token)
                if not context.complete:
                    return
                username = str(context.initiator_name)
                user = self.get_user_from_username(username)
                user.gssresponse = base64.b64encode(response).decode('utf-8')
                return user
            except gssapi.exceptions.GSSError as e:
                logger.warning('GSSAPI Error: %s', e, exc_info=settings.DEBUG)
                return
            except (binascii.Error, TypeError):
                logger.warning('GSSAPI Error: Invalid base64 encoded token provided')
                return

            return


class SpnegoModelBackend(SpnegoBackendMixin, ModelBackend):

    @classmethod
    def get_user_from_username(cls, username):
        model = get_user_model()
        try:
            user, _ = model.objects.get_or_create(username=username.split('@')[0])
            return user
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            return

        return