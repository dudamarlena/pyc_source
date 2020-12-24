# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/urls.py
# Compiled at: 2009-10-31 23:36:37
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()
from account.openid_consumer import PinaxConsumer
from blog.feeds import BlogFeedAll, BlogFeedUser
from bookmarks.feeds import BookmarkFeed
from microblogging.feeds import TweetFeedAll, TweetFeedUser, TweetFeedUserWithFriends
import os.path
tweets_feed_dict = {'feed_dict': {'all': TweetFeedAll, 
                 'only': TweetFeedUser, 
                 'with_friends': TweetFeedUserWithFriends}}
blogs_feed_dict = {'feed_dict': {'all': BlogFeedAll, 
                 'only': BlogFeedUser}}
bookmarks_feed_dict = {'feed_dict': {'': BookmarkFeed}}
if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = 'account.views.signup'
else:
    signup_view = 'signup_codes.views.signup'
urlpatterns = patterns('', url('^$', direct_to_template, {'template': 'homepage.html'}, name='home'), url('^admin/invite_user/$', 'signup_codes.views.admin_invite_user', name='admin_invite_user'), url('^account/signup/$', signup_view, name='acct_signup'), (
 '^about/', include('about.urls')), (
 '^account/', include('account.urls')), (
 '^openid/(.*)', PinaxConsumer()), (
 '^bbauth/', include('bbauth.urls')), (
 '^authsub/', include('authsub.urls')), (
 '^profiles/', include('profiles.urls')), (
 '^blog/', include('blog.urls')), (
 '^tags/', include('tag_app.urls')), (
 '^invitations/', include('friends_app.urls')), (
 '^notices/', include('notification.urls')), (
 '^messages/', include('messages.urls')), (
 '^announcements/', include('announcements.urls')), (
 '^tweets/', include('microblogging.urls')), (
 '^tribes/', include('tribes.urls')), (
 '^comments/', include('threadedcomments.urls')), (
 '^robots.txt$', include('robots.urls')), (
 '^i18n/', include('django.conf.urls.i18n')), (
 '^bookmarks/', include('bookmarks.urls')), (
 '^admin/doc/', include('django.contrib.admindocs.urls')), (
 '^admin/', include(admin.site.urls)), (
 '^photos/', include('photos.urls')), (
 '^avatar/', include('avatar.urls')), (
 '^swaps/', include('swaps.urls')), (
 '^flag/', include('flag.urls')), (
 '^locations/', include('locations.urls')), (
 '^feeds/tweets/(.*)/$', 'django.contrib.syndication.views.feed', tweets_feed_dict), (
 '^feeds/posts/(.*)/$', 'django.contrib.syndication.views.feed', blogs_feed_dict), (
 '^feeds/bookmarks/(.*)/?$', 'django.contrib.syndication.views.feed', bookmarks_feed_dict))
from photos.models import Image
friends_photos_kwargs = {'template_name': 'photos/friends_photos.html', 
   'friends_objects_function': lambda users: Image.objects.filter(member__in=users)}
from blog.models import Post
friends_blogs_kwargs = {'template_name': 'blog/friends_posts.html', 
   'friends_objects_function': lambda users: Post.objects.filter(author__in=users)}
from microblogging.models import Tweet
friends_tweets_kwargs = {'template_name': 'microblogging/friends_tweets.html', 
   'friends_objects_function': lambda users: Tweet.objects.filter(sender_id__in=[ user.id for user in users ], sender_type__name='user')}
from bookmarks.models import Bookmark
friends_bookmarks_kwargs = {'template_name': 'bookmarks/friends_bookmarks.html', 
   'friends_objects_function': lambda users: Bookmark.objects.filter(saved_instances__user__in=users), 
   'extra_context': {'user_bookmarks': lambda request: Bookmark.objects.filter(saved_instances__user=request.user)}}
urlpatterns += patterns('', url('^photos/friends_photos/$', 'friends_app.views.friends_objects', kwargs=friends_photos_kwargs, name='friends_photos'), url('^blog/friends_blogs/$', 'friends_app.views.friends_objects', kwargs=friends_blogs_kwargs, name='friends_blogs'), url('^tweets/friends_tweets/$', 'friends_app.views.friends_objects', kwargs=friends_tweets_kwargs, name='friends_tweets'), url('^bookmarks/friends_bookmarks/$', 'friends_app.views.friends_objects', kwargs=friends_bookmarks_kwargs, name='friends_bookmarks'))
if settings.SERVE_MEDIA:
    urlpatterns += patterns('', (
     '^site_media/', include('staticfiles.urls')))
from satchmo_store.urls import shoppatterns, basepatterns
urlpatterns += basepatterns + shoppatterns
urlpatterns += patterns('', url('^', include('cms.urls')))