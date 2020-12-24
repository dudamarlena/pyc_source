# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/lib/python2.7/site-packages/eloqua/settings.py
# Compiled at: 2013-02-25 05:04:09
import logging
logger = logging.getLogger(__name__)
try:
    from django.conf import settings
except ImportError:
    settings = {}

SITE = getattr(settings, 'ELOQUA_SITE', None)
USERNAME = getattr(settings, 'ELOQUA_USERNAME', None)
PASSWORD = getattr(settings, 'ELOQUA_PASSWORD', None)
BASE_URL = getattr(settings, 'ELOQUA_BASE_URL', 'https://secure.eloqua.com/API/REST/1.0')
PROFILE_TIMEOUT = getattr(settings, 'ELOQUA_PROFILE_TIMEOUT', 86400)