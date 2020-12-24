# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/global_untranslated_placeholder/models.py
# Compiled at: 2018-03-27 09:45:07
# Size of source mod 2**32: 910 bytes
from django.conf import settings
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from .conf import UntranslatedPlaceholderConf
from .signals import *

def content_renderer__init__(self, request):
    self.__original_init__(request)
    global_untranslated = getattr(settings, 'DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS', None)
    if global_untranslated:
        if global_untranslated in settings.LANGUAGES:
            self.request_language = global_untranslated
    else:
        self.request_language = settings.LANGUAGE_CODE


ContentRenderer.__original_init__ = ContentRenderer.__init__
ContentRenderer.__init__ = content_renderer__init__