# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sessions/base_session.py
# Compiled at: 2019-02-14 00:35:16
"""
This module allows importing AbstractBaseSession even
when django.contrib.sessions is not in INSTALLED_APPS.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

class BaseSessionManager(models.Manager):

    def encode(self, session_dict):
        """
        Return the given session dictionary serialized and encoded as a string.
        """
        session_store_class = self.model.get_session_store_class()
        return session_store_class().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        s = self.model(session_key, self.encode(session_dict), expire_date)
        if session_dict:
            s.save()
        else:
            s.delete()
        return s


@python_2_unicode_compatible
class AbstractBaseSession(models.Model):
    session_key = models.CharField(_(b'session key'), max_length=40, primary_key=True)
    session_data = models.TextField(_(b'session data'))
    expire_date = models.DateTimeField(_(b'expire date'), db_index=True)
    objects = BaseSessionManager()

    class Meta:
        abstract = True
        verbose_name = _(b'session')
        verbose_name_plural = _(b'sessions')

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_store_class(cls):
        raise NotImplementedError

    def get_decoded(self):
        session_store_class = self.get_session_store_class()
        return session_store_class().decode(self.session_data)