# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/urls.py
# Compiled at: 2013-05-25 17:32:37
from django.conf.urls import *
from django.views.generic import TemplateView
from vellum.feeds import PostFeed, CategoryFeed, TagFeed
from vellum.views import *
urlpatterns = patterns('', url('^(?P<year>\\d{4})/(?P<month>\\d{2})/(?P<day>\\d{1,2})/(?P<slug>[-\\w]+)/$', view=PostView.as_view(), name='vellum_detail'), url('^(?P<year>\\d{4})/(?P<month>\\d{2})/(?P<day>\\d{1,2})/$', view=PostDayArchiveView.as_view(), name='vellum_archive_day'), url('^(?P<year>\\d{4})/(?P<month>\\d{2})/$', view=PostMonthArchiveView.as_view(), name='vellum_archive_month'), url('^(?P<year>\\d{4})/$', view=PostYearArchiveView.as_view(), name='vellum_archive_year'), url('^categories/(?P<slug>[^/]+)/feed$', view=CategoryFeed(), name='vellum_category_feed'), url('^categories/(?P<slug>[-\\w]+)/$', view=CategoryDetailView.as_view(), name='vellum_category_detail'), url('^categories/$', view=CategoryListView.as_view(), name='vellum_category_list'), url('^tags/(?P<slug>[^/]+)/feed$', view=TagFeed(), name='vellum_tag_feed'), url('^tags/(?P<slug>[-\\w]+)/$', view=TagDetailView.as_view(), name='vellum_tag_detail'), url('^tags/$', view=TemplateView.as_view(template_name='vellum/tag_list.html'), name='vellum_tag_list'), url('^search/$', view=search, name='vellum_search'), url('^archives/$', view=PostArchiveView.as_view(), name='vellum_archives'), url('^feed/$', view=PostFeed(), name='vellum_feed'), url('^$', view=PostIndexView.as_view(), name='vellum'))