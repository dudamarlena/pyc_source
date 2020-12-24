# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/settings.py
# Compiled at: 2013-08-22 16:11:06
from django.conf import settings
FEED_TITLE = getattr(settings, 'CHALK_FEED_TITLE', 'Article Feed1')
FEED_DESCRIPTION = getattr(settings, 'CHALK_FEED_DESCRIPTION', 'All Articles1')
DOCUTILS_OVERRIDES = {'syntax_highlight': 'short', 
   'initial_header_level': 2, 
   'doctitle_xform': False}
DOCUTILS_OVERRIDES.update(getattr(settings, 'CHALK_DOCUTILS_OVERRIDES', {}))