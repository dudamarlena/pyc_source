# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/urls.py
# Compiled at: 2012-02-14 23:34:00
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()
if settings.BOOKI_MAINTENANCE_MODE:
    urlpatterns = patterns('', url('^admin/', include(admin.site.urls)), url('^.*$', 'booki.portal.views.maintenance', name='maintenance'))
else:
    from booki.portal import feeds
    urlpatterns = patterns('', url('^admin/', include(admin.site.urls)), url('^$', 'booki.portal.views.view_frontpage', name='frontpage'), (
     '^favicon\\.ico', 'django.views.generic.simple.redirect_to', {'url': '/site_static/images/favicon.png'}), (
     '^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}), (
     '^site_static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_STATIC_ROOT, 'show_indexes': True}), (
     '^data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DATA_ROOT, 'show_indexes': True}), ('^debug/redis/$',
                                                                                                                        'booki.portal.views.debug_redis'), url('list-groups/', 'booki.portal.views.view_groups'), url('list-books/', 'booki.portal.views.view_books'), url('list-people/', 'booki.portal.views.view_people'), url('^list-books.json$', 'booki.editor.views.view_books_json'), url('^list-books-by-id/(?P<scheme>[\\w. -]+).json?$', 'booki.portal.views.view_books_by_id'), url('^accounts/', include('booki.account.urls')), url('^feeds/rss/book/(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.BookFeedRSS()), url('^feeds/atom/book/(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.BookFeedAtom()), url('^feeds/rss/chapter/(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/(?P<chapterid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.ChapterFeedRSS()), url('^feeds/atom/chapter/(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/(?P<chapterid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.ChapterFeedAtom()), url('^feeds/rss/user/(?P<userid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.UserFeedRSS()), url('^feeds/atom/user/(?P<userid>[\\w\\s\\_\\.\\-\\d]+)/$', feeds.UserFeedAtom()), url('^groups/(?P<groupid>[\\w\\s\\_\\.\\-]+)/add_book/$', 'booki.portal.views.add_book'), url('^groups/(?P<groupid>[\\w\\s\\_\\.\\-]+)/remove_book/$', 'booki.portal.views.remove_book'), url('^groups/(?P<groupid>[\\w\\s\\_\\.\\-]+)/$', 'booki.portal.views.view_group', name='view_group'), url('^_utils/profilethumb/(?P<profileid>[\\w\\d\\_\\.\\-]+)/thumbnail.jpg$', 'booki.account.views.view_profilethumbnail', name='view_profilethumbnail'), url('^_utils/profileinfo/(?P<profileid>[\\w\\d\\_\\.\\-]+)/$', 'booki.utils.pages.profileinfo', name='view_profileinfo'), url('^_utils/attachmentinfo/(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/(?P<version>[\\w\\d\\.\\-]+)/(?P<attachment>.*)$', 'booki.utils.pages.attachmentinfo'), (
     '^robots.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}), url('^export/(?P<bookid>[\\w\\s\\_\\.\\-]+)/export/{0,1}$', 'booki.editor.views.export', name='export_booki'), url('^_sputnik/$', 'sputnik.views.dispatcher', {'map': (
             ('^/booki/$', 'booki.channels.main'),
             ('^/booki/book/(?P<bookid>\\d+)/(?P<version>[\\w\\d\\.\\-]+)/$', 'booki.channels.editor'),
             ('^/booki/profile/(?P<profileid>.+)/$', 'booki.channels.profile'),
             ('^/booki/group/(?P<groupid>.+)/$', 'booki.channels.group'),
             ('^/chat/(?P<bookid>\\d+)/$', 'booki.channels.chat'))}), url('^messaging/', include('booki.messaging.urls')), url('^(?P<bookid>[\\w\\s\\_\\.\\-\\d]+)/', include('booki.editor.urls')))