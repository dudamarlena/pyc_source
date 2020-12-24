# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\david\Projects\cosmicdb\cosmicdb\urls.py
# Compiled at: 2018-05-13 00:21:23
# Size of source mod 2**32: 2316 bytes
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, password_change_done, password_reset_done, password_reset_complete
from cosmicdb.views import CosmicLoginView, CosmicSignupView, CosmicPasswordResetView, CosmicPasswordResetConfirmView, CosmicPasswordChangeView, Home, Dashboard, notifications, messages, CosmicChangeEmail
favicon_view = RedirectView.as_view(url=(static('cosmicdb/img/favicon.ico')), permanent=True)
urlpatterns = [
 url('^admin/', admin.site.urls),
 url('^login/$', (CosmicLoginView.as_view()), name='login'),
 url('^logout/$', logout, name='logout'),
 url('^password_change/$', (CosmicPasswordChangeView.as_view()), name='password_change'),
 url('^password_change_done/$', password_change_done, name='password_change_done'),
 url('^password_reset/$', (CosmicPasswordResetView.as_view()), name='password_reset'),
 url('^password_reset_done/$', password_reset_done, name='password_reset_done'),
 url('^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', (CosmicPasswordResetConfirmView.as_view()), name='password_reset_confirm'),
 url('^password_reset_complete/$', password_reset_complete, name='password_reset_complete'),
 url('^email_change/$', (login_required(CosmicChangeEmail.as_view())), name='email_change'),
 url('^favicon\\.ico$', favicon_view, name='favicon_default'),
 url('^$', (Home.as_view()), name='home'),
 url('^dashboard/$', (login_required(Dashboard.as_view())), name='dashboard'),
 url('^notifications/$', notifications, name='notifications'),
 url('^notifications/(?P<id>[0-9]+)/$', notifications, name='notifications'),
 url('^messages/$', messages, name='messages'),
 url('^messages/(?P<id>[0-9]+)/$', messages, name='messages')]
if hasattr(settings, 'COSMICDB_ALLOW_SIGNUP'):
    if settings.COSMICDB_ALLOW_SIGNUP:
        urlpatterns = urlpatterns + [
         url('^signup/$', (CosmicSignupView.as_view()), name='signup')]