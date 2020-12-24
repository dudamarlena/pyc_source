# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/social/urls.py
# Compiled at: 2011-08-22 06:58:14
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('^add-friend/(?P<user_id>\\d+)/$', 'social.views.add_friend', name='social_add_friend'), url('^remove-friend/(?P<user_id>\\d+)/$', 'social.views.remove_friend', name='social_remove_friend'), url('^invitation-confirm/done/$', 'social.views.invitation_confirm_done', name='social_invitation_confirm_done'), url('^invitation-confirm/(?P<invitation_id>\\d+)/$', 'friends.views.respond_to_friendship_invitation', {'redirect_to_view': 'social_invitation_confirm_done'}, name='social_invitation_confirm'))