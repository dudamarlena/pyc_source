# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/tinymce/settings.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 895 bytes
import os
from django.conf import settings
import tendenci.apps.theme.templatetags.static as static
DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {'theme':'simple', 
 'relative_urls':False})
USE_SPELLCHECKER = getattr(settings, 'TINYMCE_SPELLCHECKER', False)
USE_COMPRESSOR = getattr(settings, 'TINYMCE_COMPRESSOR', False)
USE_FILEBROWSER = getattr(settings, 'TINYMCE_FILEBROWSER', 'filebrowser' in settings.INSTALLED_APPS)
if 'staticfiles' in settings.INSTALLED_APPS or 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    JS_URL = static(getattr(settings, 'TINYMCE_JS_URL', 'tiny_mce/tiny_mce.js'))
else:
    JS_URL = getattr(settings, 'TINYMCE_JS_URL', '%sjs/tiny_mce/tiny_mce.js' % settings.MEDIA_URL)
    JS_ROOT = getattr(settings, 'TINYMCE_JS_ROOT', os.path.join(settings.MEDIA_ROOT, 'js/tiny_mce'))
JS_BASE_URL = JS_URL[:JS_URL.rfind('/')]