# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/hosts.py
# Compiled at: 2019-05-02 13:25:00
from __future__ import unicode_literals
from __future__ import absolute_import
from django.utils.functional import empty, SimpleLazyObject
__ALL__ = ('ALLOWED_HOSTS', 'AllowedHosts')
_wrapped_default = empty

class IterableLazyObject(SimpleLazyObject):
    _wrapped_default = globals()[b'_wrapped_default']

    def __iter__(self):
        if self._wrapped is self._wrapped_default:
            self._setup()
        return self._wrapped.__iter__()


class AllowedHosts(object):
    alias_model = None

    def __init__(self):
        from django.conf import settings
        self.extra_hosts = getattr(settings, b'MULTISITE_EXTRA_HOSTS', [])
        if self.alias_model is None:
            from .models import Alias
            self.alias_model = Alias
        return

    def __iter__(self):
        for host in self.extra_hosts:
            yield host

        for host in self.alias_model.objects.values_list(b'domain'):
            yield host[0]


ALLOWED_HOSTS = IterableLazyObject(lambda : AllowedHosts())