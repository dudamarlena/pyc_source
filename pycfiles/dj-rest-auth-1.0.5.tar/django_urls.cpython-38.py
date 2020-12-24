# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/tests/django_urls.py
# Compiled at: 2020-02-29 20:48:46
# Size of source mod 2**32: 2325 bytes
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns
try:
    from django.contrib.auth.views import logout, login, password_reset, password_change, password_reset_confirm
except ImportError:
    from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
    logout = LogoutView.as_view()
    login = LoginView.as_view()
    password_reset = PasswordResetView.as_view()
    password_change = PasswordChangeView.as_view()
    password_reset_confirm = PasswordResetConfirmView.as_view()
else:
    urlpatterns += [
     url('^logout/custom_query/$', logout, dict(redirect_field_name='follow')),
     url('^logout/next_page/$', logout, dict(next_page='/somewhere/')),
     url('^logout/next_page/named/$', logout, dict(next_page='password_reset')),
     url('^password_reset_from_email/$', password_reset, dict(from_email='staffmember@example.com')),
     url('^password_reset/custom_redirect/$', password_reset, dict(post_reset_redirect='/custom/')),
     url('^password_reset/custom_redirect/named/$', password_reset, dict(post_reset_redirect='password_reset')),
     url('^password_reset/html_email_template/$', password_reset, dict(html_email_template_name='registration/html_password_reset_email.html')),
     url('^reset/custom/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, dict(post_reset_redirect='/custom/')),
     url('^reset/custom/named/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, dict(post_reset_redirect='password_reset')),
     url('^password_change/custom/$', password_change, dict(post_change_redirect='/custom/')),
     url('^password_change/custom/named/$', password_change, dict(post_change_redirect='password_reset')),
     url('^admin_password_reset/$', password_reset, dict(is_admin_site=True)),
     url('^login_required/$', login_required(password_reset)),
     url('^login_required_login_url/$', login_required(password_reset, login_url='/somewhere/'))]