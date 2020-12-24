# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/validators.py
# Compiled at: 2018-03-13 16:19:41
# Size of source mod 2**32: 341 bytes
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def http_port_validator(value):
    parsed = urlparse(value)
    if parsed.port not in (None, 80, 443):
        raise ValidationError(_('URL port is not a common HTTP port'))