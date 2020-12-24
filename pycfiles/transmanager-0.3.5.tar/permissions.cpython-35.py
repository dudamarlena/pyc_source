# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/permissions.py
# Compiled at: 2016-06-02 03:35:45
# Size of source mod 2**32: 854 bytes
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
logger = logging.getLogger(__name__)

class AuthenticationMixin(object):
    __doc__ = '\n    Mixin to check that the user has the translator profile\n    '
    translator_user = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            authorized = True
        else:
            try:
                self.translator_user = request.user.translator_user
                authorized = True
            except ObjectDoesNotExist:
                authorized = False

        if not authorized:
            return redirect(reverse_lazy('index'))
        return super(AuthenticationMixin, self).dispatch(request, *args, **kwargs)