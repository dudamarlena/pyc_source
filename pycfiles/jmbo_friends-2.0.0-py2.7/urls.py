# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/friends/urls.py
# Compiled at: 2015-04-29 09:47:05
from django.conf.urls import patterns, url, include
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth.decorators import login_required
from friends import views, forms
urlpatterns = patterns('', url('^members/(?P<username>[=@\\.\\w+-]+)/$', views.MemberDetail.as_view(form_class=forms.SendDirectMessageInlineForm, template_name='friends/member_detail.html'), name='member-detail'), url('^friend-request/(?P<member_id>\\d+)/$', login_required(views.friend_request), {}, name='friend-request'), url('^my-friends/$', login_required(views.MyFriends.as_view(template_name='friends/my_friends.html')), name='my-friends'), url('^my-friend-requests/$', login_required(views.MyFriendRequests.as_view(template_name='friends/my_friend_requests.html')), name='my-friend-requests'), url('^accept-friend-request/(?P<memberfriend_id>\\d+)/$', login_required(views.accept_friend_request), {}, name='accept-friend-request'), url('^de-friend/(?P<member_id>\\d+)/$', login_required(views.de_friend), {}, name='de-friend'), url('^inbox/$', login_required(views.Inbox.as_view(template_name='friends/inbox.html')), name='inbox'), url('^message/send/$', login_required(views.SendDirectMessage.as_view(form_class=forms.SendDirectMessageForm, template_name='friends/send_direct_message.html')), name='send-direct-message'), url('^message/(?P<pk>\\d+)/view/$', login_required(views.ViewMessage.as_view(template_name='friends/message_view.html')), name='message-view'), url('^message/(?P<pk>\\d+)/reply/$', login_required(views.ReplyToDirectMessage.as_view(form_class=forms.ReplyToDirectMessageForm, template_name='friends/reply_to_direct_message.html')), name='reply-to-direct-message'))