# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/__init__.py
# Compiled at: 2020-02-25 03:29:17
# Size of source mod 2**32: 771 bytes
import logging
LOGGER = logging.getLogger(__name__)
DEFAULT_SETTINGS = [
 'CHOICES_SEPARATOR',
 'USER_DID_NOT_ANSWER',
 'TEX_CONFIGURATION_FILE',
 'SURVEY_DEFAULT_PIE_COLOR',
 'EXCEL_COMPATIBLE_CSV',
 'DEFAULT_SURVEY_PUBLISHING_DURATION']

def set_default_settings():
    try:
        from django.conf import settings
        from . import settings as app_settings
        for setting in dir(app_settings):
            if setting in DEFAULT_SETTINGS:
                if not hasattr(settings, setting):
                    setattr(settings, setting, getattr(app_settings, setting))
                LOGGER.info("Settings '%s' as the default ('%s')", setting, getattr(settings, setting))

    except ImportError:
        pass


set_default_settings()