# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/diary_urls.py
# Compiled at: 2012-07-20 05:27:44
from django.conf import settings
from django.conf.urls.defaults import *
from django.views import generic
from dress_blog.models import Diary
from dress_blog.views import DiaryDetailView, DiaryRedirectView
page_size = getattr(settings, 'DRESS_BLOG_PAGINATE_BY', 28)
urlpatterns = patterns('', url('^(?P<year>\\d{4})/(?P<month>\\w{3})/(?P<day>\\d{1,2})/$', DiaryDetailView.as_view(model=Diary, date_field='pub_date', month_format='%b'), name='blog-diary-detail'), url('^$', DiaryRedirectView.as_view(), name='blog-diary'))