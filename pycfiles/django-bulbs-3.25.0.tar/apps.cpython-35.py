# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/apps.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 224 bytes
from django.apps import AppConfig

class LiveBlogConfig(AppConfig):
    name = 'bulbs.liveblog'

    def ready(self):
        import bulbs.liveblog.signals