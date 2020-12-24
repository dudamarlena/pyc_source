# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/app_registry.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 713 bytes
from tendenci.apps.registry.sites import site
from tendenci.apps.registry.base import AppRegistry
from tendenci.apps.videos.models import Video

class VideoRegistry(AppRegistry):
    version = '1.0'
    author = 'Tendenci - The Open Source AMS for Associations'
    author_email = 'programmers@tendenci.com'
    description = 'Add video and display them in a grid format'
    event_logs = {'video': {'base':('1200000', '993355'), 
               'add':('1200100', '119933'), 
               'edit':('1200200', 'EEDD55'), 
               'delete':('1200300', 'AA2222'), 
               'search':('1200400', 'CC55EE'), 
               'view':('1200500', '55AACC')}}


site.register(Video, VideoRegistry)