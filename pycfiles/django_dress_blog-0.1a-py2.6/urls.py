# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/urls.py
# Compiled at: 2012-07-20 05:27:44
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import DetailView, ListView, TemplateView
from tagging.models import Tag
from django_comments_xtd.models import XtdComment
from dress_blog import views
from dress_blog.models import BlogRoll
from dress_blog.feeds import LatestPostsFeed, LatestStoriesFeed, LatestQuotesFeed, LatestDiaryDetailsFeed, PostsByTag
from dress_blog.sitemaps import PostsSitemap
page_size = getattr(settings, 'DRESS_BLOG_PAGINATE_BY', 10)
ui_columns = getattr(settings, 'DRESS_BLOG_UI_COLUMNS', 3)
urlpatterns = patterns('', url('^stories/', include('dress_blog.story_urls')), url('^diary/', include('dress_blog.diary_urls')), url('^quotes/', include('dress_blog.quote_urls')), url('^blogroll$', ListView.as_view(model=BlogRoll, queryset=BlogRoll.objects.all().order_by('sort_order'), template_name='dress_blog/blogroll.html', paginate_by=2 * page_size), name='blog-blogroll'), url('^tags$', TemplateView.as_view(template_name='dress_blog/tag_list.html'), name='blog-tag-list'), url('^tags/(?P<slug>.{1,50})$', views.TagDetailView.as_view(), name='blog-tag-detail'), url('^comments$', ListView.as_view(queryset=XtdComment.objects.for_app_models('dress_blog.story', 'dress_blog.quote', 'dress_blog.diarydetail'), template_name='dress_blog/comment_list.html', paginate_by=page_size), name='blog-comment-list'), url('^post/(\\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='post-url-redirect'), url('^feeds/posts/$', LatestPostsFeed(), name='latest-posts-feed'), url('^feeds/stories/$', LatestStoriesFeed(), name='latest-stories-feed'), url('^feeds/quotes/$', LatestQuotesFeed(), name='latest-quotes-feed'), url('^feeds/diary/$', LatestDiaryDetailsFeed(), name='latest-diary-feed'), url('^feeds/comments/$', LatestCommentFeed(), name='comments-feed'), url('^feeds/tag/(?P<slug>.{1,50})$', PostsByTag(), name='posts-tagged-as'))
from haystack.forms import SearchForm
from haystack.views import SearchView, search_view_factory
urlpatterns += patterns('', url('^search$', search_view_factory(view_class=SearchView, form_class=SearchForm, results_per_page=page_size), name='haystack-search'))
if ui_columns == 4:
    urlpatterns += patterns('', url('^$', views.index, name='blog-index'))
else:
    urlpatterns += patterns('', url('^$', views.PostListView.as_view(), name='blog-index'))