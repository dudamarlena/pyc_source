# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/validators.py
# Compiled at: 2020-03-12 04:44:12
# Size of source mod 2**32: 1286 bytes
import os
from django.core.exceptions import ValidationError
import django.utils.translation as _
from weblate.fonts.utils import get_font_name

def validate_font(value):
    """Simple extension based validation for uploads."""
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in ('.ttf', '.otf'):
        raise ValidationError(_('Unsupported file format.'))
    try:
        get_font_name(value)
    except OSError:
        raise ValidationError(_('Unsupported file format.'))

    return value