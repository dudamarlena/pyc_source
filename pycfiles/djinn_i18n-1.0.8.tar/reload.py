# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/views/reload.py
# Compiled at: 2015-10-30 06:39:55
from django.contrib import messages
from djinn_core.views.admin import AdminMixin
from index import IndexView

class ReloadView(IndexView, AdminMixin):

    def get(self, request, *args, **kwargs):
        from django.utils import translation
        from django.utils.translation import trans_real
        try:
            from threading import local
        except ImportError:
            from django.utils._threading_local import local

        _thread_locals = local()
        import gettext
        try:
            gettext._translations = {}
            trans_real._translations = {}
            trans_real._default = None
            messages.add_message(request, messages.SUCCESS, 'Translations reloaded')
            prev = trans_real._active.pop(_thread_locals, None)
            if prev:
                translation.activate(prev.language())
        except AttributeError as e:
            pass

        return super(ReloadView, self).get(request, *args, **kwargs)