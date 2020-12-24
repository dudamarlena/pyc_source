# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/managers.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.conf import settings
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models

class CurrentSiteManager(models.Manager):
    """Use this to limit objects to those associated with the current site."""
    use_in_migrations = True

    def __init__(self, field_name=None):
        super(CurrentSiteManager, self).__init__()
        self.__field_name = field_name

    def check(self, **kwargs):
        errors = super(CurrentSiteManager, self).check(**kwargs)
        errors.extend(self._check_field_name())
        return errors

    def _check_field_name(self):
        field_name = self._get_field_name()
        try:
            field = self.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return [
             checks.Error(b"CurrentSiteManager could not find a field named '%s'." % field_name, obj=self, id=b'sites.E001')]

        if not field.many_to_many and not isinstance(field, models.ForeignKey):
            return [
             checks.Error(b"CurrentSiteManager cannot use '%s.%s' as it is not a foreign key or a many-to-many field." % (
              self.model._meta.object_name, field_name), obj=self, id=b'sites.E002')]
        return []

    def _get_field_name(self):
        """ Return self.__field_name or 'site' or 'sites'. """
        if not self.__field_name:
            try:
                self.model._meta.get_field(b'site')
            except FieldDoesNotExist:
                self.__field_name = b'sites'
            else:
                self.__field_name = b'site'

        return self.__field_name

    def get_queryset(self):
        return super(CurrentSiteManager, self).get_queryset().filter(**{self._get_field_name() + b'__id': settings.SITE_ID})