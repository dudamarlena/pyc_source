# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/plugins/player.py
# Compiled at: 2013-12-03 16:20:29
from flask import render_template_string

class Player(object):
    has_panel = False
    button_index = 100
    button_label = ''
    index_template = '\n{% if stat %}\n    {% if stat.state in (2, 3) %}\n        {% if current_song.is_stream %}\n            [Stream]\n            {{ current_song.title }}\n        {% else %}\n            {{ current_song.formatted_title|safe }}\n        {% endif %}\n        <br />\n\n        <table>\n            <tr>\n                <td>\n                    <a id=\'sb\' onclick=\'seekclick(event);\'><div id=\'sbc\' style=\'width:{{percent_time*2}}px\'></div></a>\n                </td>\n                <td>\n                    {{percent_time|int}}% - {{"%02d:%02d"|format(elapsed_time/60, elapsed_time%60)}}/{{"%02d:%02d"|format(total_time/60, total_time%60)}}\n                </td>\n            </tr>\n        </table>\n    {% endif %}\n{% else %}\nError : Can\'t play that!\n{% endif %}\n\n<button onclick=\'execute_plugin("player", "prev", {}, refresh_player);\'><<</button>\n{% if stat.state != 2 %}\n    <button onclick=\'execute_plugin("player", "play", {}, refresh_player);\'>></button>\n{% else %}\n    <button onclick=\'execute_plugin("player", "pause", {}, refresh_player);\'>||</button>\n{% endif %}\n{% if stat.state != 1 %}\n    <button onclick=\'execute_plugin("player", "stop", {}, refresh_player);\'>[]</button>\n{% endif %}\n\n<button onclick=\'execute_plugin("player", "next", {}, refresh_player);\'>>></button>\n\n{% if has_stream %}\n<button onclick=\'audio_playstop();\'>[>]</button>\n{% endif %}\n\n{% if stat.state != 0 and stat.volume != -1 %}\n    <button onclick=\'execute_plugin("player", "volume_down", {}, refresh_player);\'>-</button>\n    <button onclick=\'execute_plugin("player", "volume_up", {}, refresh_player);\'>+</button>\n    <button onclick=\'execute_plugin("player", "mute", {}, refresh_player);\'>@</button>\n    {{ stat.volume }}%\n{% endif %}\n'
    playlist_template = '\n<h2>Playlist ({{ total_index }})\n    <button onclick=\'execute_plugin("player", "clear", {}, refresh_player);\'>clear</button>\n    <button onclick=\'execute_plugin("player", "clear_old", {}, refresh_player);\'>clear old</button>\n    <button onclick=\'execute_plugin("player", "shuffle", {}, refresh_player);\'>shuffle</button>\n</h2>\n\n{% for index, entry in enumerate(playlist) %}\n    <li \n    {% if current_index == index+1 %}\n        class=\'s\'\n    {% else %}\n        {{ loop.cycle("", "class=\'p\'") }}\n    {% endif %}\n    > {{ "%03d"|format(index) }}\n        <a href=\'#\' onclick=\'execute_plugin("player", "delete", {idx: {{index}} }, refresh_player);\'><span>X</span></a>\n        <a href=\'#\' onclick=\'execute_plugin("player", "play", {idx: {{index}} }, refresh_player);\'>{{ entry.formatted_title }}</a>\n    </li>\n{% endfor %}\n\n'

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self):
        stat = self.mpd.status()
        if stat.state in (2, 3):
            elapsed_time, total_time, percent_time = self.mpd.getSongPosition()
        else:
            elapsed_time, total_time, percent_time = (0, 0, 0)
        return render_template_string(self.index_template, stat=stat, current_song=self.mpd.getCurrentSong(self.config['tag_format']), elapsed_time=elapsed_time, total_time=total_time, percent_time=percent_time, has_stream=self.config['has_stream'])

    def playlist(self):
        current_index, total_index = self.mpd.getPlaylistPosition()
        return render_template_string(self.playlist_template, current_index=current_index, total_index=total_index, playlist=self.mpd.playlist(self.config['tag_format']), enumerate=enumerate)

    def ajax_play(self, idx=None):
        if idx:
            self.mpd.play(int(idx))
        else:
            self.mpd.play()

    def ajax_delete(self, idx=None):
        self.mpd.delete([int(idx)])

    def ajax_next(self):
        self.mpd.next()

    def ajax_prev(self):
        self.mpd.prev()

    def ajax_pause(self):
        self.mpd.pause()

    def ajax_playpause(self):
        stat = self.mpd.status()
        if stat.state != 2:
            self.mpd.play()
        else:
            self.mpd.pause()

    def ajax_stop(self):
        self.mpd.stop()

    def ajax_clear(self):
        self.mpd.clear()

    def ajax_clear_old(self):
        idx, tot = self.mpd.getPlaylistPosition()
        self.mpd.delete([[0, max(0, idx - 2)]])

    def ajax_shuffle(self):
        self.mpd.shuffleIt()

    def ajax_seek(self, percent=None):
        self.mpd.seek(percent=int(percent))

    def ajax_volume_up(self):
        self.mpd.volumeUp()

    def ajax_volume_down(self):
        self.mpd.volumeDown()

    def ajax_mute(self):
        self.mpd.mute()

    def ajax_change_display(self, idx=None):
        self.mpd.changeDisplay(int(idx))