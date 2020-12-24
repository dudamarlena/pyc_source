# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sf_www/mezzanine/personal/heroku/o/personal/portfolio/urls.py
# Compiled at: 2016-12-17 17:50:41
# Size of source mod 2**32: 1459 bytes
from django.conf.urls import url
from portfolio import views
from mezzanine.conf import settings
_slash = '/' if settings.APPEND_SLASH else ''
urlpatterns = [
 url('^tag/(?P<tag>.*)%s$' % _slash, views.portfolio_post_list, name='portfolio_post_list_tag'),
 url('^category/(?P<category>.*)%s$' % _slash, views.portfolio_post_list, name='portfolio_post_list_category'),
 url('^author/(?P<username>.*)%s$' % _slash, views.portfolio_post_list, name='portfolio_post_list_author'),
 url('^archive/(?P<year>\\d{4})/(?P<month>\\d{1,2})%s$' % _slash, views.portfolio_post_list, name='portfolio_post_list_month'),
 url('^archive/(?P<year>\\d{4})%s$' % _slash, views.portfolio_post_list, name='portfolio_post_list_year'),
 url('^(?P<year>\\d{4})/(?P<month>\\d{1,2})/(?P<day>\\d{1,2})/(?P<slug>.*)%s$' % _slash, views.portfolio_post_detail, name='portfolio_post_detail_day'),
 url('^(?P<year>\\d{4})/(?P<month>\\d{1,2})/(?P<slug>.*)%s$' % _slash, views.portfolio_post_detail, name='portfolio_post_detail_month'),
 url('^(?P<year>\\d{4})/(?P<slug>.*)%s$' % _slash, views.portfolio_post_detail, name='portfolio_post_detail_year'),
 url('^(?P<slug>.*)%s$' % _slash, views.portfolio_post_detail, name='portfolio_post_detail'),
 url('^$', views.portfolio_post_list, name='portfolio_post_list')]