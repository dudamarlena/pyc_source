# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/requests.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class RequestSite(object):
    """
    A class that shares the primary interface of Site (i.e., it has
    ``domain`` and ``name`` attributes) but gets its data from a Django
    HttpRequest object rather than from a database.

    The save() and delete() methods raise NotImplementedError.
    """

    def __init__(self, request):
        self.domain = self.name = request.get_host()

    def __str__(self):
        return self.domain

    def save(self, force_insert=False, force_update=False):
        raise NotImplementedError(b'RequestSite cannot be saved.')

    def delete(self):
        raise NotImplementedError(b'RequestSite cannot be deleted.')