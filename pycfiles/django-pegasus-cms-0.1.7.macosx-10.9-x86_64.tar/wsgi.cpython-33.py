# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/wsgi.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 493 bytes
from __future__ import absolute_import, division
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pegasus.settings.prod')
application = get_wsgi_application()