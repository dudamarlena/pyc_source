# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/lib/python2.7/site-packages/richtext_blog/urls.py
# Compiled at: 2012-04-18 09:57:56
try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

from richtext_blog.views import PostListView, PostView, TagView, AllPostsRssFeed, AllPostsAtomFeed, RedirectToPostsView
urlpatterns = patterns('', url('^$', RedirectToPostsView.as_view(permanent=True)), url('^posts/$', PostListView.as_view(paginate_by=10, template_name='richtext_blog/post-list.html'), name='posts_all'), url('^(?P<year>[\\d]{4})/$', PostListView.as_view(paginate_by=10, template_name='richtext_blog/post-list.html'), name='posts_yearly'), url('^(?P<year>[\\d]{4})/(?P<month>[\\d]{2})/$', PostListView.as_view(paginate_by=10, template_name='richtext_blog/post-list.html'), name='posts_monthly'), url('^(?P<year>[\\d]{4})/(?P<month>[\\d]{2})/(?P<slug>[-\\w]+)/$', PostView.as_view(template_name='richtext_blog/post-detail.html'), name='post'), url('^tags/(?P<slug>[-\\w]+)/$', TagView.as_view(template_name='richtext_blog/tag-view.html'), name='posts_tag'), url('^rss/$', AllPostsRssFeed(), name='posts_all_rss'), url('^atom/$', AllPostsAtomFeed(), name='posts_all_atom'))