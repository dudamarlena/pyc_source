# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/BLOG/workon/templatetags/workon_compress.py
# Compiled at: 2018-01-29 03:08:41
# Size of source mod 2**32: 423 bytes
from django.conf import settings
__all__ = [
 'lazy_register']

def lazy_register(register):
    if 'compressor' in settings.INSTALLED_APPS:

        @register.tag
        def compress(parser, token):
            from compressor.templatetags.compress import compress
            return compress(parser, token)

    else:
        try:

            @register.to_end_tag
            def compress(parsed, context, token):
                return parsed

        except:
            pass