# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/rb_platform.py
# Compiled at: 2020-02-11 04:03:56
"""Global configuration for deployment paths and settings.

These values may need to be modified for deployment on different operating
system platforms. Packagers should review this file and patch it appropriately
for their systems.
"""
from __future__ import unicode_literals
SITELIST_FILE_UNIX = b'/etc/reviewboard/sites'
DEFAULT_FS_CACHE_PATH = b'/tmp/reviewboard_cache'
INSTALLED_SITE_PATH = b'/var/www'