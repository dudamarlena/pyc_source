# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/django_avem_theme/avem_theme/context.py
# Compiled at: 2019-11-08 15:35:12
# Size of source mod 2**32: 285 bytes
from django.conf import settings

def base_template(request):
    """
        Make the base template available everywhere for extending.
        """
    if getattr(settings, 'BASE_TEMPLATE', None):
        base = settings.BASE_TEMPLATE
    else:
        base = 'avem/base.html'
    return {'BASE_TEMPLATE': base}