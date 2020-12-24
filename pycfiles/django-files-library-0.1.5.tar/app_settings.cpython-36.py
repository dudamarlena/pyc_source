# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/app_settings.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 923 bytes


class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings, 'ALLAUTH_SETTING_GETTER', lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    @property
    def ADD_FILE_FORM_CLASS(self):
        """
        Add file form
        """
        return self._setting('ADD_FILE_FORM_CLASS', None)

    @property
    def INLINE_FORM(self):
        """
        Add file form
        """
        return self._setting('INLINE_FORM', False)


import sys
app_settings = AppSettings('DJANGO_FILES_LIBRARY_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings