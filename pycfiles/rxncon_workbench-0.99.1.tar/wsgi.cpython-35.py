# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mathias/tbp/django_rxncon_site/src/rxncon_site/wsgi.py
# Compiled at: 2018-06-27 10:02:27
# Size of source mod 2**32: 586 bytes
"""
WSGI config for rxncon_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
try:
    import rxncon_site.import_tester
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rxncon_site.settings')
except ImportError:
    import src.rxncon_site.import_tester
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.rxncon_site.settings')

application = get_wsgi_application()