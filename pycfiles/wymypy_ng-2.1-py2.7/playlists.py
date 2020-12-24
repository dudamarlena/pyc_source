# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/playlists.py
# Compiled at: 2013-12-02 15:53:24
from flask import render_template_string

class Playlists(object):
    has_panel = True
    button_index = 2
    button_label = 'Playlists'
    index_template = '\n<h2>Playlists</h2>\n\n{% for playlist in playlists %}\n    <li {{ loop.cycle("", "class=\'p\'") }}><a href="#" onclick=\'execute_plugin("playlists", "load", {playlist: "{{ playlist.path }}"}, refresh_player);\'>{{ playlist.path }}</a></li> \n{% endfor %}\n'

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self):
        return render_template_string(self.index_template, playlists=self.mpd.getPlaylistNames())

    def ajax_load(self, playlist):
        self.mpd.load(playlist)