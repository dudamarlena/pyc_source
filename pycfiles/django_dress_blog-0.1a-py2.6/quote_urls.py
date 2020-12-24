# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/quote_urls.py
# Compiled at: 2012-07-20 05:27:44
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from dress_blog.models import Quote
from dress_blog.views import PostDetailView
page_size = getattr(settings, 'DRESS_BLOG_PAGINATE_BY', 2)
large_page_size = getattr(settings, 'DRESS_BLOG_PAGINATE_BY', 2) * 2
urlpatterns = patterns('', url('^(?P<year>\\d{4})/(?P<month>\\d{1,2})/(?P<day>\\d{1,2})/(?P<slug>[-\\w]+)/$', PostDetailView.as_view(model=Quote, date_field='pub_date', month_format='%m', template_name='blog/quote_detail.html'), name='blog-quote-detail-month-numeric'), url('^(?P<year>\\d{4})/(?P<month>\\w{3})/(?P<day>\\d{1,2})/(?P<slug>[-\\w]+)/$', PostDetailView.as_view(model=Quote, date_field='pub_date', month_format='%b', template_name='blog/quote_detail.html'), name='blog-quote-detail'), url('^(?P<year>\\d{4})/(?P<month>\\w{3})/(?P<day>\\d{1,2})/(?P<slug>[-\\w]+)/draft/$', login_required(generic.DateDetailView.as_view(model=Quote, date_field='pub_date', month_format='%b', template_name='blog/quote_detail.html', allow_future=True)), name='blog-quote-detail-draft'), url('^(?P<year>\\d{4})/(?P<month>\\d{1,2})/(?P<day>\\d{1,2})/$', generic.DayArchiveView.as_view(model=Quote, date_field='pub_date', month_format='%m', paginate_by=page_size), name='blog-quote-archive-day'), url('^(?P<year>\\d{4})/(?P<month>\\d{1,2})/$', generic.MonthArchiveView.as_view(model=Quote, date_field='pub_date', month_format='%m', paginate_by=page_size), name='blog-quote-archive-month'), url('^(?P<year>\\d{4})/$', generic.YearArchiveView.as_view(model=Quote, date_field='pub_date', make_object_list=True, paginate_by=large_page_size), name='blog-quote-archive-year'), url('^$', generic.ListView.as_view(queryset=Quote.objects.published(), template_name='dress_blog/quote_list.html', paginate_by=page_size), name='blog-quote-list'))