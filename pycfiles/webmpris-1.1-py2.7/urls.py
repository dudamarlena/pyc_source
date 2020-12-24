# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webmpris/urls.py
# Compiled at: 2013-11-14 22:46:20
from django.conf.urls import patterns, url
from webmpris.views import Root, Player, TrackList, Playlists
OBJ_MAP = {'Root': Root, 'Player': Player, 
   'TrackList': TrackList, 
   'Playlists': Playlists}
urlpatterns = patterns('webmpris.views', url('^players$', 'get_players', name='players'))
for name, obj in OBJ_MAP.items():
    url_prop = ('^players/(?P<player_id>:[\\w.]+)/{name}$').format(name=name)
    url_meth = url_prop[:-1] + '/(?P<method_name>[\\w]+$)'
    urlpatterns += patterns('', url(url_prop, obj.as_view()), url(url_meth, obj.as_view()))