# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/echelon/conf.py
# Compiled at: 2011-09-24 06:25:11
from django.conf import settings
base = getattr(settings, 'ECHELON_CONFIG', {})
TITLE = base.get('TITLE', 'Echelon')
NAME = base.get('NAME', 'Echelon')
MEDIA_PREFIX = base.get('MEDIA_PREFIX', None)
BASE_URL = base.get('BASE_URL')