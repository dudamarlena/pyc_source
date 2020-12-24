# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Rich/Sites/django-applepodcast/podcast/tests/urls.py
# Compiled at: 2017-07-17 15:18:58
# Size of source mod 2**32: 131 bytes
from django.conf.urls import url, include
urlpatterns = [
 url('^podcast/', include('podcast.urls', namespace='podcast'))]