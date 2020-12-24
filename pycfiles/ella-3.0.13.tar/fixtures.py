# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_photos/fixtures.py
# Compiled at: 2013-07-03 05:00:55
from django.conf import settings
from django.contrib.sites.models import Site
from ella.photos.models import Format
from ella.utils.test_helpers import create_photo
__all__ = ('create_photo_formats', )

def create_photo_formats(case):
    case.basic_format = Format(name='basic', max_width=20, max_height=20, flexible_height=False, stretch=False, nocrop=False, resample_quality=85)
    case.basic_format.save()
    case.basic_format.sites.add(Site.objects.get(pk=getattr(settings, 'SITE_ID', 1)))