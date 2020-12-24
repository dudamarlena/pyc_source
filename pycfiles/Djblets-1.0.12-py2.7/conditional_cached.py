# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/template/loaders/conditional_cached.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.conf import settings
from django.template.loaders import cached

class Loader(cached.Loader):
    """Caches template loading results only if not in DEBUG mode.

    This extends Django's built-in 'cached' template loader to only
    perform caching if ``settings.DEBUG`` is False. That helps to keep
    the site nice and speedy when in production, without causing headaches
    during development.
    """

    def load_template(self, *args, **kwargs):
        if settings.DEBUG:
            self.reset()
        return super(Loader, self).load_template(*args, **kwargs)