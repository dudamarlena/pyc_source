# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/postgres/fields/citext.py
# Compiled at: 2019-02-14 00:35:16
from django.db.models import CharField, EmailField, TextField
__all__ = ['CICharField', 'CIEmailField', 'CIText', 'CITextField']

class CIText(object):

    def get_internal_type(self):
        return 'CI' + super(CIText, self).get_internal_type()

    def db_type(self, connection):
        return 'citext'


class CICharField(CIText, CharField):
    pass


class CIEmailField(CIText, EmailField):
    pass


class CITextField(CIText, TextField):
    pass