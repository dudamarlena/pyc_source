# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/common/api_urls.py
# Compiled at: 2016-09-24 12:17:50
# Size of source mod 2**32: 599 bytes
from django.conf.urls import url, include
from cms.router import urls as router_urls
from cms.nav import urls as nav_urls
from cms.content import urls as content_urls
from cms.accounts import urls as accounts_urls
from cms.emails import urls as emails_urls
from cms.live_admin import urls as live_admin_urls
urlpatterns = [
 url('^route/', include(router_urls)),
 url('^nav/', include(nav_urls)),
 url('^content/', include(content_urls)),
 url('^accounts/', include(accounts_urls)),
 url('^emails/', include(emails_urls)),
 url('^live-admin/', include(live_admin_urls))]