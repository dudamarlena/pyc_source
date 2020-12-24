# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/settings.py
# Compiled at: 2015-12-05 18:17:38
try:
    from django.conf import django_settings
except (ImportError, NameError) as e:
    django_settings = None

STRICT = getattr(django_settings, 'PDF_MINER_IS_STRICT', True)